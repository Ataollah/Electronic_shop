import pytest
from django.utils import timezone
from datetime import timedelta
from order.models import Order
from order.tasks import cancel_unpaid_orders
from appuser.tests.appuser_fixtures import app_user,customer_user

@pytest.mark.django_db
def test_cancel_unpaid_orders(customer_user):
    # Create an unpaid order older than 24 hours
    old_order = Order.objects.create(
        user=customer_user,
        status='unpaid'
    )
    old_order.created_at = timezone.now() - timedelta(hours=25)
    old_order.save()
    # Create a recent unpaid order
    recent_order = Order.objects.create(
        user=customer_user,
        status='unpaid'
    )

    print('recent_order : ', recent_order.created_at)
    print('old_order : ', old_order.created_at)
    # Create a paid order older than 24 hours
    paid_order = Order.objects.create(
        user=customer_user,
        status='paid'
    )
    paid_order.created_at = timezone.now() - timedelta(hours=25)
    paid_order.save()

    cancel_unpaid_orders()

    old_order.refresh_from_db()
    recent_order.refresh_from_db()
    paid_order.refresh_from_db()

    assert old_order.status == 'canceled'
    assert recent_order.status == 'unpaid'
    assert paid_order.status == 'paid'