from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from Accounts.models import Profile, PayHistory
from django.urls import reverse
from Accounts.forms import SignUpForm, ChangeForm
import re

from Store.models import Receipt


def sing_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=password)
            login(request, user)
            profile = Profile.objects.get_or_create(user=request.user, username_id=username)
            return HttpResponseRedirect(reverse('Store:product'))
    else:
        form = SignUpForm()
    context = {'form': form}
    return render(request, 'Accounts/sign_up.html', context)


def login_view(request):
    context = {

    }
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is None:
            context['error'] = 'username or password is wrong'
            return render(request, 'Accounts/login.html', context)
        else:
            login(request, user)
            return HttpResponseRedirect(reverse('Store:product'))

    else:
        return render(request, 'Accounts/login.html', context)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('Account:login'))


def main_view(request):
    return HttpResponse('hello word')


def profile_detail(request):
    profile = request.user.profile
    return render(request, 'Accounts/profile.html', {'profile': profile})


def pay_view(request):
    profile = request.user.profile
    context = {'profile': profile}
    if request.method == 'POST':
        try:
            number = int(request.POST['number'])
            receipt = request.POST['receipt']
            assert re.match(r'^bank\d{4}\$', receipt), 'receipt is not correct!'
            assert 0 < number < 1000, 'The the amount of money is not correct!'
            PayHistory.objects.create(number=number, customer=profile)
            profile.balance += number
            profile.save()
            context['suc'] = 'The payment is successfully and %i$ add to your account' % number
        except Exception as e:
            context['error'] = str(e)
    bal = profile.balance
    context['bal'] = bal
    context['pays'] = PayHistory.objects.filter(customer=profile).order_by('-time')

    return render(request, 'Accounts/pay.html', context)


def purchase(request):
    # profile = request.user.profile
    receipts = Receipt.objects.filter(customer=request.user.profile).order_by('-buy_time')
    return render(request, 'Accounts/purchase.html', {'res': receipts})


def edit_profile(request):
    if request.method == 'POST':
        result = ChangeForm(request.POST, instance=request.user)
        if result.is_valid():
            result.save()
            return HttpResponseRedirect(reverse('Account:profile_detail'))
    else:
        result = ChangeForm(instance=request.user)
    context = {'result': result}
    return render(request, "Accounts/edit.html", context)


from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes


def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "password/password_reset_email.txt"
                    c = {
                        "email": user.email,
                        'domain': '127.0.0.1:8000',
                        'site_name': 'Website',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'fifa19.900t@gmail.com', [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect("/password_reset/done/")
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="password/password_reset.html",
                  context={"password_reset_form": password_reset_form})
