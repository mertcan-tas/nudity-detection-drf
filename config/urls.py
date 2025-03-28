from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('account.urls')),
    path('api/', include('app.urls')),
    path('api/', include('authentication.urls')),
]

if settings.DEBUG:
    urlpatterns.append(path('testing/', include('testing.urls')))
    urlpatterns.append(path('api/schema/', SpectacularAPIView.as_view(), name='schema'))
    urlpatterns.append(path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),)