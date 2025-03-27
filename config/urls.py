from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('account.urls')),
    path('api/', include('authentication.urls')),
]

if settings.DEBUG:
    urlpatterns.append(path('testing/', include('testing.urls')))