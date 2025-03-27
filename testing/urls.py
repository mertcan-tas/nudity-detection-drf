from django.contrib.auth import login
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.http import HttpResponse

from django.urls import path
from testing.views import NoAuthTokenView

User = get_user_model()

def AutoLoginAdmin(request):
    user = User.objects.filter(is_superuser=True).first()
    if user:
        login(request, user)
        return redirect('/admin/')
    return HttpResponse("Admin kullanıcı bulunamadı.")

urlpatterns = [
    path('admin/login/', AutoLoginAdmin),
    path('no-auth/', NoAuthTokenView.as_view(), name='basic'),
]