from django.urls import path
from authorization.views import (CustomUserCreateView, CustomUserRetrieveView, CheckAdminView,
                                 AdminListView, ApproveUserView, RejectUserView)

urlpatterns = [
    path("users/", CustomUserCreateView.as_view(), name="user-create"),
    path("user-info/", CustomUserRetrieveView.as_view(), name="user-info"),
    path("check-admin/", CheckAdminView.as_view(), name="check-admin"),
    path("all-admins/", AdminListView.as_view(), name="all-admins"),
    path("user-approve/<int:telegram_id>/", ApproveUserView.as_view(), name="approve-user"),
    path("user-reject/<int:telegram_id>/", RejectUserView.as_view(), name="reject-user"),
]