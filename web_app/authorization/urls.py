from django.urls import path
from authorization.views import (CustomUserCreateView, CustomUserRetrieveView, CheckAdminView,
                                 AdminListView, ApproveUserView, RejectUserView, SetUserLevelView,
                                 WaitingApprovedUsersListView, WaitingStatusUsersListView, 
                                 OrderConfirmedView, OrderRejectedView, WaitingConfirmOrdersListView, 
                                 WaitingShippingOrdersListView, OrderDeliveredView, OrderHistoryView)
from authorization.telegram_auth import TelegramWebAppAuthView, CheckAuthStatusView, UserInfoView

urlpatterns = [
    path("users/", CustomUserCreateView.as_view(), name="user-create"),
    path("user-info/", CustomUserRetrieveView.as_view(), name="user-info"),
    path("check-admin/", CheckAdminView.as_view(), name="check-admin"),
    path("all-admins/", AdminListView.as_view(), name="all-admins"),
    path("user-approve/<int:telegram_id>/", ApproveUserView.as_view(), name="approve-user"),
    path("user-reject/<int:telegram_id>/", RejectUserView.as_view(), name="reject-user"),
    path("user-set-level/<int:telegram_id>/", SetUserLevelView.as_view(), name="set-user-level"),
    path('waiting-approved-users/', WaitingApprovedUsersListView.as_view(), name='waiting-approved-users'),
    path('waiting-status-users/', WaitingStatusUsersListView.as_view(), name='waiting-status-users'),
    
    # Telegram Web App Authentication
    path("telegram-auth/", TelegramWebAppAuthView.as_view(), name="telegram-auth"),
    path("auth-status/", CheckAuthStatusView.as_view(), name="auth-status"), 
    path("user-profile/", UserInfoView.as_view(), name="user-profile"),

    #orders
    path("order-confirm/<int:order_id>/", OrderConfirmedView.as_view(), name="order-confirmed"),
    path("order-reject/<int:order_id>/", OrderRejectedView.as_view(), name="order-rejected"),
    path("order-delivered/<int:order_id>/", OrderDeliveredView.as_view(), name="order-delivered"),
    path("order-last-10/", OrderHistoryView.as_view(), name="order-last-10"),
    
    path('waiting-confirm-orders/', WaitingConfirmOrdersListView.as_view(), name='waiting-confirm-orders'),
    path('waiting-shipping-orders/', WaitingShippingOrdersListView.as_view(), name='waiting-shipping-orders'),

]