import pytest
from order.models import *

@pytest.fixture
def order(db, app_user):
    return Order.objects.create(
        user=app_user,
        total_amount=50000,
        discount=5000,
        status='unpaid',
        description='Test order',
        province='تهران',
        county='تهران',
        district='مرکزی',
        city='تهران',
        rural='',
        address='Test address',
        postal_code='1234567890'
    )

@pytest.fixture
def order_item(db, order, product):
    return OrderItems.objects.create(
        order=order,
        product=product,
        quantity=3,
        price=20000
    )


@pytest.fixture
def order_payment(db, order):
    return OrderPayment.objects.create(
        order=order,
        amount=100000,
        transaction_id='TX123456',
        authority='AUTH123456',
        status='paid'
    )