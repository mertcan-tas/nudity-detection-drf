from django.urls import path

from rest_framework_simplejwt.views import TokenObtainPairView
from authentication.views import RegisterEmailView, PasswordChangeView

urlpatterns = [ 
    path('auth/login/', TokenObtainPairView.as_view(), name='email-login'),
    path('auth/register/', RegisterEmailView.as_view(), name='email-register'),
    path('auth/change-password/', PasswordChangeView.as_view(), name='change-password'),
]
