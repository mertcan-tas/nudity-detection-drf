from django.urls import path

from account.views import UserDetailView

urlpatterns = [    
    path("user/detail/", UserDetailView.as_view(), name="user-detail"),
]