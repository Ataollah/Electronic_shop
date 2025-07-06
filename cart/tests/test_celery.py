import pytest
from django.utils import timezone
from datetime import timedelta
from cart.models import CartItem, Cart
from cart.tasks import remove_expired_cart_items
from appuser.tests.appuser_fixtures import app_user,customer_user
from product.test_product.test_product_fixture import product,category

@pytest.mark.django_db
def test_remove_expired_cart_items(customer_user,product):
    cart= Cart.objects.create(user=customer_user)
    now = timezone.now()

    expired = CartItem.objects.create(
        cart=cart,
        product=product,
        price=10000,
        quantity=2,
        expires_at=now - timedelta(hours=1)
    )
    not_expired = CartItem.objects.create(
        cart=cart,
        product=product,
        price=10000,
        quantity=2,
        expires_at=now + timedelta(hours=1)
    )


    remove_expired_cart_items()

    assert not CartItem.objects.filter(id=expired.id).exists()
    assert CartItem.objects.filter(id=not_expired.id).exists()