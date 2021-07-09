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
            return render(request, 'accounts/login.html', context)
        else:
            login(request, user)
            return HttpResponseRedirect(reverse('Store:product'))

    else:
        return render(request, 'accounts/login.html', context)


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
