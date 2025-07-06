from django.urls import path
from .views import *

app_name = 'zarinpal'

urlpatterns = [
    path('request/', SendRequestView.as_view(), name='send-request'),
    path('verify/', VerifyRequestView.as_view() , name='verify-payment'),
    path('server-error/', ServerErrorView.as_view(), name='server-error-view'),
]
