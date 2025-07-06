from django.urls import path
from .views import *

urlpatterns = [
    path('dashboard/', DashboardHomeView.as_view(), name='customer-dashboard'),
    path('profile/', ProfileView.as_view(), name='customer-profile'),
    path('address/',UpdateUserAddressView.as_view(), name='customer-update-address'),
    path('order-history/', OrderHistoryView.as_view(), name='customer-order-history'),
    path('order-history-status/<str:status>/', OrderHistoryByStatusView.as_view(), name='customer-order-history-status'),
    path('order-details/<int:order_id>/', OrderDetailView.as_view(), name='customer-order-details'),
    path('change-password/', ChangePasswordView.as_view(), name='customer-change-password'),
]