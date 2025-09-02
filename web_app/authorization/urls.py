from django.urls import path
from authorization.views import CustomUserCreateView, CustomUserRetrieveView

urlpatterns = [
    path("users/", CustomUserCreateView.as_view(), name="user-create"),
    path("user-info/", CustomUserRetrieveView.as_view(), name="user-info"),
]