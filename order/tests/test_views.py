import pytest
from django.urls import reverse
from cart.models import Cart, CartItem
from iran.models import Province
from order.models import Order, OrderItems
from product.models import Product
from appuser.tests.appuser_fixtures import app_user,customer_user,cashier_user

@pytest.mark.django_db
def test_place_order_view_creates_order_and_redirects(client, customer_user):
    user = customer_user
    client.force_login(user)
    cart = Cart.objects.create(user=user)
    product = Product.objects.create(title='Test Product', inventory=10)
    CartItem.objects.create(cart=cart, product=product, price=1000, quantity=2)

    url = reverse('place-order')  # Adjust to your URL name
    response = client.get(url)

    # Check redirect to checkout
    assert response.status_code == 302
    assert response.url == reverse('checkout')

    # Check order and order items created
    order = Order.objects.get(user=user)
    assert order.total_amount == 2000
    assert OrderItems.objects.filter(order=order).count() == 1

    # Cart should be empty
    assert not CartItem.objects.filter(cart=cart).exists()


@pytest.mark.django_db
def test_update_order_address_view_updates_address(client, customer_user):
    user = customer_user
    client.force_login(user)
    province = Province.objects.create(name='TestProvince')
    order = Order.objects.create(user=user, province=province)
    session = client.session
    session['order_id'] = order.id
    session.save()

    url = reverse('update-order-address')  # Adjust to your URL name
    data = {
        'province': province.id,
        'county': 'TestCounty',
        'district': 'TestDistrict',
        'city': 'TestCity',
        'rural': 'TestRural',
        'address': 'Test Address',
        'postal_code': '1234567890'
    }
    response = client.post(url, data)
    assert response.status_code == 302
    assert response.url == reverse('checkout')

    order.refresh_from_db()
    assert order.county == 'TestCounty'
    assert order.city == 'TestCity'
    assert order.address == 'Test Address'

@pytest.mark.django_db
def test_update_order_address_view_redirects_without_order_id(client, customer_user):
    user = customer_user
    client.force_login(user)
    url = reverse('update-order-address')  # Adjust to your URL name
    response = client.post(url, {})
    assert response.status_code == 302
    assert response.url == reverse('cart-items')


@pytest.mark.django_db
def test_checkout_view_get_with_order_id(client, customer_user):
    user = customer_user
    client.force_login(user)
    province = Province.objects.create(name='TestProvince')
    order = Order.objects.create(user=user, province=province)
    session = client.session
    session['order_id'] = order.id
    session.save()
    print('order_is : ',order.id)

    url = reverse('checkout')
    response = client.get(url)
    assert response.status_code == 200
    assert b'order' in response.content  # Adjust as needed for your template

@pytest.mark.django_db
def test_checkout_view_get_without_order_id(client, customer_user):
    user = customer_user
    client.force_login(user)
    url = reverse('checkout')
    response = client.get(url)
    assert response.status_code == 302
    assert response.url == reverse('cart-items')

@pytest.mark.django_db
def test_checkout_view_post_valid_form(client, customer_user):
    user = customer_user
    client.force_login(user)
    province = Province.objects.create(name='TestProvince')
    order = Order.objects.create(user=user, province=province)
    session = client.session
    session['order_id'] = order.id
    session.save()

    url = reverse('checkout')
    data = {'description': 'Test order'}
    response = client.post(url, data)
    assert response.status_code == 302
    assert response.url == reverse('zarinpal:send-request')
    order.refresh_from_db()
    assert order.description == 'Test order'


@pytest.mark.django_db
def test_update_order_address_view_updates_address(client, customer_user):
    user = customer_user
    client.force_login(user)
    province = Province.objects.create(name='TestProvince')
    order = Order.objects.create(user=user, province=province)
    session = client.session
    session['order_id'] = order.id
    session.save()

    url = reverse('update-order-address')  # Adjust to your URL name
    data = {
        'province': province.id,
        'county': 'TestCounty',
        'district': 'TestDistrict',
        'city': 'TestCity',
        'rural': 'TestRural',
        'address': 'Test Address',
        'postal_code': '1234567890'
    }
    response = client.post(url, data)
    assert response.status_code == 302
    assert response.url == reverse('checkout')

    order.refresh_from_db()
    assert order.county == 'TestCounty'
    assert order.city == 'TestCity'
    assert order.address == 'Test Address'

@pytest.mark.django_db
def test_update_order_address_view_redirects_without_order_id(client, customer_user):
    user = customer_user
    client.force_login(user)
    url = reverse('update-order-address')  # Adjust to your URL name
    response = client.post(url, {})
    assert response.status_code == 302
    assert response.url == reverse('cart-items')


@pytest.mark.django_db
def test_cancel_order_view_sets_status_and_restores_inventory(client, customer_user):
    user = customer_user
    client.force_login(user)
    product = Product.objects.create(title='Test Product', inventory=5)
    order = Order.objects.create(user=user, status='paid', total_amount=1000)
    OrderItems.objects.create(order=order, product=product, quantity=2, price=500)

    url = reverse('cancel-order-view', kwargs={'order_id': order.id})  # Adjust URL name if needed
    response = client.get(url)

    order.refresh_from_db()
    product.refresh_from_db()
    assert order.status == 'canceled'
    assert product.inventory == 7  # 5 + 2
    assert response.status_code == 302
    assert response.url == reverse('customer-order-history')

@pytest.mark.django_db
def test_resume_payment_view_sets_order_id_and_redirects(client, customer_user):
    user = customer_user
    client.force_login(user)
    province = Province.objects.create(name='TestProvince')
    order = Order.objects.create(user=user, province=province)

    url = reverse('resume-payment-view', kwargs={'order_id': order.id})  # Adjust URL name if needed
    response = client.get(url)

    # Check session and redirect
    session = client.session
    assert session['order_id'] == order.id
    assert response.status_code == 302
    assert response.url == reverse('checkout')

@pytest.mark.django_db
def test_payment_failed_view_renders_template(client, customer_user):
    user = customer_user
    client.force_login(user)
    url = reverse('payment-failed-view')  # Adjust if your URL name differs
    response = client.get(url)
    assert response.status_code == 200
    assert 'پرداخت  ناموفق'.encode('utf-8') in response.content  # Adjust if your template content differs


@pytest.mark.django_db
def test_payment_failed_view_requires_login(client):
    url = reverse('payment-failed-view')
    response = client.get(url)
    assert response.status_code == 302  # Redirect to login


@pytest.mark.django_db
def test_payment_succeeded_view_renders_template_and_context(client, customer_user):
    user = customer_user
    client.force_login(user)
    province = Province.objects.create(name='TestProvince')
    order = Order.objects.create(user=user, province=province)
    session = client.session
    session['order_id'] = order.id
    session.save()

    url = reverse('payment-succeeded-view')  # Adjust if your URL name differs
    response = client.get(url)
    assert response.status_code == 200
    assert 'پرداخت موفق'.encode('utf-8') in response.content  # Adjust if your template content differs
    assert response.context['order'] == order

@pytest.mark.django_db
def test_payment_succeeded_view_requires_login(client):
    url = reverse('payment-succeeded-view')
    response = client.get(url)
    assert response.status_code == 302  # Redirect to login