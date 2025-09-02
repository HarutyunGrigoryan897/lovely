from django.urls import path
from authorization.views import (CustomUserCreateView, CustomUserRetrieveView, CheckAdminView,
                                 AdminListView, ApproveUserView, RejectUserView)
from authorization.telegram_auth import TelegramWebAppAuthView, CheckAuthStatusView, UserInfoView

urlpatterns = [
    path("users/", CustomUserCreateView.as_view(), name="user-create"),
    path("user-info/", CustomUserRetrieveView.as_view(), name="user-info"),
    path("check-admin/", CheckAdminView.as_view(), name="check-admin"),
    path("all-admins/", AdminListView.as_view(), name="all-admins"),
    path("user-approve/<int:telegram_id>/", ApproveUserView.as_view(), name="approve-user"),
    path("user-reject/<int:telegram_id>/", RejectUserView.as_view(), name="reject-user"),
    
    # Telegram Web App Authentication
    path("telegram-auth/", TelegramWebAppAuthView.as_view(), name="telegram-auth"),
    path("auth-status/", CheckAuthStatusView.as_view(), name="auth-status"), 
    path("user-profile/", UserInfoView.as_view(), name="user-profile"),
]