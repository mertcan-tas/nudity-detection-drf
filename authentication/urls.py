from django.urls import path

from authentication.views import LoginAPIView, RegisterAPIView, PasswordChangeView

urlpatterns = [ 
    path('auth/login/', LoginAPIView.as_view(), name='email-login'),
    path('auth/register/', RegisterAPIView.as_view(), name='email-register'),
    path('auth/change-password/', PasswordChangeView.as_view(), name='change-password'),
]
