from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from order.models import Order

@shared_task
def cancel_unpaid_orders():
    cutoff = timezone.now() - timedelta(hours=24)
    orders = Order.objects.filter(status='unpaid', created_at__lt=cutoff)
    print('orders to cancel:', orders.count())
    for order in orders:
        print('order : ',order)
    count = orders.update(status='canceled')
    # send sms to user
    return f'Canceled {count} unpaid orders older than 24 hours.'