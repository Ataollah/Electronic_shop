from django.urls import path
from .views import *

app_name = 'cashier'

urlpatterns = [
    path('dashboard/', DashboardHomeView.as_view(), name='dashboard'),
    path('order-by-status/<str:status>/', OrdersByStatusView.as_view(), name='order-by-status'),
    path('order-details/<int:order_id>/', OrderDetailView.as_view(), name='order-details'),
    path('change-order-status/<int:order_id>/', ChangeOrderStatusView.as_view(), name='change-order-status'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('toggle-selling/',ToggleSellingView.as_view(), name='toggle-selling'),

]