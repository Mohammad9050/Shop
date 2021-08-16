from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include

from Shop import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('Accounts.urls')),
    path('', include('Store.urls')),
    url('^', include('django.contrib.auth.urls'))

]
#if settings.DEBUG:
  #  from django.conf.urls.static import static

  #  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
