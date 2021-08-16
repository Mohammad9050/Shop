from django.urls import path
from . import views
from django.views.generic import TemplateView
app_name = 'Account'
urlpatterns = [
    path('sign_up', views.sing_up, name='signup'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('main_test', views.main_view, name='main_test'),
    path('profile_detail', views.profile_detail, name ='profile_detail'),
    path('pay', views.pay_view, name='pay'),
    path('purchase', views.purchase, name='purchase'),
    path('edit', views.edit_profile, name='edit')
   # path('tetsy', TemplateView.as_view(template_name='Accounts/pay_test.html'))
]
