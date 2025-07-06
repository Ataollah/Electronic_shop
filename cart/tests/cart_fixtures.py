import pytest
from cart.models import Cart, CartItem
from appuser.tests.appuser_fixtures import app_user

@pytest.fixture
def cart(db, app_user):
    return Cart.objects.create(user=app_user)


@pytest.fixture
def cart_item(db, cart, product):
    return CartItem.objects.create(
        cart=cart,
        product=product,
        price=10000,
        quantity=2,
        expires_at=timezone.now() + timezone.timedelta(hours=2)
    )