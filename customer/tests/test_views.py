import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from appuser.tests.appuser_fixtures import cashier_user, customer_user, app_user, get_test_image
from iran.models import Province
from order.models import Order, OrderPayment


@pytest.mark.django_db
def test_dashboard_home_view_get(client, customer_user):
    client.force_login(customer_user)
    url = reverse('customer-dashboard')
    response = client.get(url)
    assert response.status_code == 200
    assert 'customer/Home/home.html' in [t.name for t in response.templates]



@pytest.mark.django_db
def test_profile_view_get(client, customer_user):
    client.force_login(customer_user)
    url = reverse('customer-profile')
    response = client.get(url)
    assert response.status_code == 200
    assert 'form' in response.context
    assert 'provinces' in response.context
    assert list(response.context['provinces']) == list(Province.objects.all())

@pytest.mark.django_db
def test_profile_view_post_valid(client, customer_user):
    client.force_login(customer_user)
    url = reverse('customer-profile')
    profile_image = get_test_image()
    data = {
        'username': customer_user.username,
        'first_name': 'NewName',
        'last_name': customer_user.last_name,
        'province': 'tehran',
        'city': 'tehran',
        'district': 'markazi',
        'email': customer_user.email,
        'county': 'tehran',
        'rural': '',
        'profile_picture': profile_image,
        'address': customer_user.address,
        'postal_code': customer_user.postal_code,
    }
    response = client.post(url, data,format='multipart')
    assert response.status_code == 200
    customer_user.refresh_from_db()
    assert customer_user.first_name == 'NewName'

@pytest.mark.django_db
def test_profile_view_post_invalid(client, customer_user):
    client.force_login(customer_user)
    url = reverse('customer-profile')
    data = {
        'username': '',  # Invalid: required field
    }
    response = client.post(url, data)
    assert response.status_code == 200
    assert 'form' in response.context
    assert response.context['form'].errors
    customer_user.refresh_from_db()
    # Ensure the username was not changed to an empty string
    assert customer_user.username != ''



@pytest.mark.django_db
def test_update_user_address_view(client, customer_user):
    client.force_login(customer_user)
    province = Province.objects.create(name='tehran')
    url = reverse('customer-update-address')  # Replace with your actual URL name
    data = {
        'province': province.name,
        'county': 'TestCounty',
        'district': 'TestDistrict',
        'city': 'TestCity',
        'rural': 'TestRural',
        'address': 'Test Address',
        'postal_code': '1234567890',
    }
    response = client.post(url, data)
    assert response.status_code == 302  # Redirect to profile
    customer_user.refresh_from_db()
    assert customer_user.address == 'Test Address'
    assert customer_user.city == 'TestCity'


@pytest.mark.django_db
def test_order_history_view(client, customer_user):
    client.force_login(customer_user)
    # Create some orders for the user
    orders = [Order.objects.create(user=customer_user) for _ in range(3)]
    url = reverse('customer-order-history')  # Replace with your actual URL name
    response = client.get(url)
    assert response.status_code == 200
    assert 'page_obj' in response.context
    # Check that the orders are in the page_obj
    page_orders = list(response.context['page_obj'].object_list)
    for order in orders:
        assert order in page_orders


@pytest.mark.django_db
def test_order_history_by_status_view(client, customer_user):
    client.force_login(customer_user)
    # Create orders with different statuses
    order1 = Order.objects.create(user=customer_user, status='pending')
    order2 = Order.objects.create(user=customer_user, status='completed')
    order3 = Order.objects.create(user=customer_user, status='pending')
    url = reverse('customer-order-history-status', kwargs={'status': 'pending'})  # Adjust URL name if needed
    response = client.get(url)
    assert response.status_code == 200
    assert 'page_obj' in response.context
    page_orders = list(response.context['page_obj'].object_list)
    assert order1 in page_orders
    assert order3 in page_orders
    assert order2 not in page_orders


@pytest.mark.django_db
def test_order_detail_view_success(client, customer_user):
    client.force_login(customer_user)
    order = Order.objects.create(user=customer_user)
    payment = OrderPayment.objects.create(order=order, amount=100)
    url = reverse('customer-order-details', kwargs={'order_id': order.id})  # Adjust URL name if needed
    response = client.get(url)
    assert response.status_code == 200
    assert 'order' in response.context
    assert response.context['order'] == order
    assert list(response.context['payments']) == [payment]

@pytest.mark.django_db
def test_order_detail_view_not_found(client, customer_user):
    client.force_login(customer_user)
    url = reverse('customer-order-details', kwargs={'order_id': 9999})  # Non-existent order
    response = client.get(url)
    # Should redirect to order history
    assert response.status_code == 302
    assert response.url == reverse('customer-order-history')


@pytest.mark.django_db
def test_change_password_view_get(client, customer_user):
    client.force_login(customer_user)
    url = reverse('customer-change-password')  # Adjust if your URL name is different
    response = client.get(url)
    assert response.status_code == 200
    assert 'form' in response.context

@pytest.mark.django_db
def test_change_password_view_post_valid(client, customer_user):
    client.force_login(customer_user)
    url = reverse('customer-change-password')
    data = {
        'old_password': 'testpass',
        'new_password1': 'newstrongpass123',
        'new_password2': 'newstrongpass123',
    }
    response = client.post(url, data)
    assert response.status_code == 302
    assert response.url == reverse('customer-dashboard')
    customer_user.refresh_from_db()
    assert customer_user.check_password('newstrongpass123')


@pytest.mark.django_db
def test_change_password_view_post_invalid(client, customer_user):
    client.force_login(customer_user)
    url = reverse('customer-change-password')
    data = {
        'old_password': 'wrongpassword',
        'new_password1': 'short',
        'new_password2': 'short',
    }
    response = client.post(url, data)
    assert response.status_code == 200
    assert 'form' in response.context
    assert response.context['form'].errors