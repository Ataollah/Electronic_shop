import pytest
from order.models import Order, OrderItems
from product.models import Product
from appuser.tests.appuser_fixtures import app_user,customer_user

@pytest.mark.django_db
def test_order_save_canceled_restores_inventory(customer_user):
    user = customer_user
    product = Product.objects.create(title='Test Product', inventory=5)
    order = Order.objects.create(user=user, status='paid', total_amount=1000)
    item = OrderItems.objects.create(order=order, product=product, quantity=3, price=1000)

    # Simulate status change to 'canceled'
    order.status = 'canceled'
    order.save()

    product.refresh_from_db()
    assert product.inventory == 8  # 5 + 3