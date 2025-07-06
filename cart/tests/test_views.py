import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test import Client
from unittest.mock import patch
from product.models import Product
from cart.models import Cart, CartItem
from appuser.tests.appuser_fixtures import customer_user, app_user
from product.test_product.test_product_fixture import product,category

@pytest.mark.django_db
def test_add_to_cart_view_adds_new_item(customer_user):
    client = Client()
    client.force_login(customer_user)
    product = Product.objects.create(title='Test Product', inventory=10, current_price=10000)
    url = reverse('add-to-cart')  # Make sure your urls.py has name='add-to-cart' for AddToCartView
    with patch('cart.views.getSiteInfo') as mock_site_info:
        mock_site_info.return_value.is_selling = True
        response = client.post(url, {'product_id': product.id, 'qty': 2})
        assert response.status_code == 302
        assert response.url == reverse('cart-items')
        cart = Cart.objects.get(user=customer_user)
        cart_item = CartItem.objects.get(cart=cart, product=product)
        assert cart_item.quantity == 2
        product.refresh_from_db()
        assert product.inventory == 8

@pytest.mark.django_db
def test_add_to_cart_view_increases_quantity(customer_user):
    client = Client()
    client.force_login(customer_user)
    product = Product.objects.create(title='Test Product', inventory=10, current_price=10000)
    cart = Cart.objects.create(user=customer_user)
    cart_item = CartItem.objects.create(cart=cart, product=product, price=10000, quantity=1)
    url = reverse('add-to-cart')
    with patch('cart.views.getSiteInfo') as mock_site_info:
        mock_site_info.return_value.is_selling = True
        response = client.post(url, {'product_id': product.id, 'qty': 3})
        assert response.status_code == 302
        cart_item.refresh_from_db()
        assert cart_item.quantity == 4
        product.refresh_from_db()
        assert product.inventory == 7

@pytest.mark.django_db
def test_add_to_cart_view_not_selling(customer_user):
    client = Client()
    client.force_login(customer_user)
    product = Product.objects.create(title='Test Product', inventory=10, current_price=10000)
    url = reverse('add-to-cart')
    with patch('cart.views.getSiteInfo') as mock_site_info:
        mock_site_info.return_value.is_selling = False
        response = client.post(url, {'product_id': product.id, 'qty': 1})
        assert response.status_code == 302
        assert response.url == reverse('home')
        assert not CartItem.objects.filter(product=product).exists()

@pytest.mark.django_db
def test_cart_view_get(customer_user,product):
    client = Client()
    client.force_login(customer_user)
    cart = Cart.objects.create(user=customer_user)
    cart_item = CartItem.objects.create(cart=cart, product=product, price=10000, quantity=2)
    url = reverse('cart-items')  # Make sure your urls.py has name='cart-items' for CartView
    response = client.get(url)
    assert response.status_code == 200
    assert 'cart_items' in response.context
    assert cart_item in response.context['cart_items']
    assert response.context['total_price'] == cart.totalPrice()

@pytest.mark.django_db
def test_cart_view_post_delete_item(customer_user):
    client = Client()
    client.force_login(customer_user)
    cart = Cart.objects.create(user=customer_user)
    product = Product.objects.create(title='Test Product',slug='test-product', inventory=10, current_price=10000)
    cart_item = CartItem.objects.create(cart=cart, product=product, price=10000, quantity=2)
    url = reverse('cart-items')
    response = client.post(url, {'cart_item_id': cart_item.id})
    assert response.status_code == 200
    assert not CartItem.objects.filter(id=cart_item.id).exists()
    # Should still render the cart page
    assert 'cart_items' in response.context
    assert response.context['total_price'] == cart.totalPrice()


@pytest.mark.django_db
def test_delete_mini_cart_item_view(client,customer_user):
    # Create user and login
    client = Client()
    client.force_login(customer_user)

    # Create product and cart
    product = Product.objects.create(title='Test', slug='test', inventory=5, current_price=100)
    cart = Cart.objects.create(user=customer_user)
    cart_item = CartItem.objects.create(product=product, cart=cart, price=100, quantity=1)

    # Send POST request to delete cart item
    url = reverse('delete-mini-cart-item')  # Update with your actual URL name
    response = client.post(url, {'cart_item_id': cart_item.id})

    # Assert cart item is deleted and response is a redirect
    assert response.status_code == 302
    assert not CartItem.objects.filter(id=cart_item.id).exists()


@pytest.mark.django_db
def test_delete_all_cart_items_view(client,customer_user):
    # Create user and login
    client = Client()
    client.force_login(customer_user)

    # Create product and cart with items
    product = Product.objects.create(title='Test', slug='test', inventory=5, current_price=100)
    cart = Cart.objects.create(user=customer_user)
    CartItem.objects.create(product=product, cart=cart, price=100, quantity=1)
    CartItem.objects.create(product=product, cart=cart, price=100, quantity=2)

    # Send POST request to delete all cart items
    url = reverse('delete-all-items')  # Use your actual URL name
    response = client.post(url)

    # Assert all cart items are deleted and response is a redirect
    assert response.status_code == 302
    assert cart.items.count() == 0
