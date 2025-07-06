from django.urls import path
from .views import SubscribeSuccessView

app_name = 'newsletter'

urlpatterns = [
    path('success/', SubscribeSuccessView.as_view(), name='success'),
]