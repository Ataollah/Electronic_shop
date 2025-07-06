# cart/tasks.py
from celery import shared_task
from django.utils import timezone
from .models import CartItem

@shared_task
def remove_expired_cart_items():
    now = timezone.now()
    expired_items = CartItem.objects.filter(expires_at__lt=now)
    expired_items.delete()