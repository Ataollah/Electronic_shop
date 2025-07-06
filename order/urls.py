from order.views import *
from django.urls import path,re_path

urlpatterns = [
    path('checkout/', CheckOutView.as_view(), name='checkout'),
    path('place-order/', PlaceOrderView.as_view(), name='place-order'),
    path('update-order-address/', UpdateOrderAddressView.as_view(), name='update-order-address'),
    path('payment-failed/', PaymentFailedView.as_view(), name='payment-failed-view'),
    path('payment-succeed/', PaymentSucceededView.as_view(), name='payment-succeeded-view'),
    path('resume-payment/<int:order_id>', ResumePaymentView.as_view(), name='resume-payment-view'),
    path('cancel-order/<int:order_id>',CancelOrderView.as_view(),name='cancel-order-view'),
]
