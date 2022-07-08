from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from taggit.models import Tag
from django.db.models import Count
from Accounts.models import Cart
from Store.forms import SearchForm
from Store.models import Product, Receipt


def product(request, tag_slug=None):

    find = SearchForm(request.GET)
    products = Product.objects.all()

    try:
        profile = request.user.profile
        buys = Receipt.objects.filter(customer=profile)
        tags = buys.values_list('product__tags', flat=True)
        buys_id = buys.values_list('product__id', flat=True)
        similar = Product.objects.filter(tags__in=tags).exclude(id__in=buys_id)
        similar = similar.annotate(same_tags=Count('tags')).order_by('-same_tags')[:4]
        similar_id = similar.values_list('id', flat=True)
        products = Product.objects.exclude(id__in=similar_id)
    except:
        profile = ''
        buys = []
        similar = ''
    if find.is_valid():
        name_searched = find.cleaned_data['name']
        products = products.filter(name__contains=name_searched)
        if find.cleaned_data['category'] and find.cleaned_data['category'] != 'AN':
            products = products.filter(category=find.cleaned_data['category'])
        min_price, max_price = find.get_price()
        if max_price is not None:
            products = products.filter(price__lte=max_price)
        if min_price is not None:
            products = products.filter(price__gte=min_price)
    l_product = len(products)
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        products = products.filter(tags__in=[tag])
    context = {
        'products': products,
        'find': find,
        'profile': profile,
        'l_product': l_product,
        'similar': similar
    }

    return render(request, 'Store/home.html', context)


@login_required(login_url='Accounts:login')
def add_to_cart(request, num):
    product_details = get_object_or_404(Product, pk=num)

    try:

        Cart.objects.create(customer=request.user.profile, product=product_details)
    except Exception as e:
        error = str(e)

    return HttpResponseRedirect(reverse('Store:product'))


@login_required(login_url='Accounts:login')
def cart(request):
    try:
        profile = request.user.profile
    except:
        profile = ''
    carts = Cart.objects.all()
    context = {'carts': carts, 'profile': profile}
    return render(request, 'Store/cart.html', context)


def delete_cart(request, num):
    product_details = get_object_or_404(Cart, pk=num)
    product_details.delete()
    return HttpResponseRedirect(reverse('Store:cart'))


def buy(request, num):
    profile = request.user.profile
    product_details = get_object_or_404(Cart, pk=num)
    context = {'profile': profile,
               'pro_d': product_details}
    if request.method == 'POST':
        number = int(request.POST['number'])
        try:
            total_price = number * product_details.product.price
            assert product_details.product.inventory >= number, 'Inventory is not enough!'
            assert profile.balance >= total_price, 'Money is not enough'
            product_details.product.inventory -= number
            profile.balance -= total_price
            product_details.product.save()
            profile.save()
            Receipt.objects.create(product=product_details.product, customer=request.user.profile, number=number)
            if product_details.product.inventory < 1:
                product_original = Product.objects.filter(name=product_details.product.name)
                product_original.delete()
            product_details.delete()

            return HttpResponseRedirect(reverse('Account:purchase'))
        except Exception as e:
            context['error'] = str(e)
    return render(request, 'Store/buy_page.html', context)
