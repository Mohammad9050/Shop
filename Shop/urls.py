from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from Shop import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('Accounts.urls')),
    path('', include('Store.urls')),
    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='password/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="password"
                                                                                              "/password_reset_confirm.html"),
         name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password/password_reset_complete'
                                                                                   '.html'),
         name='password_reset_complete'),

]
# if settings.DEBUG:
#  from django.conf.urls.static import static

#  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    from django.conf.urls.static import static

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
