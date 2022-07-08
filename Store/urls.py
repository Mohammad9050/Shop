from django.views.generic import TemplateView

from django.urls import path
from . import views

app_name = 'Store'
urlpatterns = [
    path('', views.product, name='product'),
    path('tag/<slug:tag_slug>', views.product, name='product'),
    path('add_to_cart/<int:num>', views.add_to_cart, name='add'),
    path('cart', views.cart, name='cart'),
    path('delete_cart/<int:num>', views.delete_cart, name='delete'),
    path('buy/<int:num>', views.buy, name='buy'),
    #path('related', views.related, name='related')
]
