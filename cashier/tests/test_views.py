import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from order.models import Order, OrderPayment
from appuser.tests.appuser_fixtures import cashier_user, customer_user,app_user
from siteInfo.test.siteInfo_fixtures import site_info



@pytest.mark.django_db
def test_dashboard_home_view_counts(client,cashier_user,customer_user):
    # Create and login user
    client.force_login(cashier_user)

    # Create orders with different statuses
    Order.objects.create(user=customer_user, status='pending')
    Order.objects.create(user=customer_user, status='paid')
    Order.objects.create(user=customer_user, status='unpaid')
    Order.objects.create(user=customer_user, status='pending')

    url = reverse('cashier:dashboard')
    response = client.get(url)

    assert response.status_code == 200
    assert response.context['pending_orders_count'] == 2
    assert response.context['paid_orders_count'] == 1
    assert response.context['unpaid_orders_count'] == 1



@pytest.mark.django_db
def test_orders_by_status_view(client, cashier_user,customer_user):
    client.force_login(cashier_user)

    # Create orders with different statuses
    Order.objects.create(user=customer_user, status='pending')
    Order.objects.create(user=customer_user, status='paid')
    Order.objects.create(user=customer_user, status='unpaid')

    # Test 'all' status
    url = reverse('cashier:order-by-status', kwargs={'status': 'all'})
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['page_obj'].paginator.count == 3

    # Test 'pending' status
    url = reverse('cashier:order-by-status', kwargs={'status': 'pending'})
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['page_obj'].paginator.count == 1

    # Test 'paid' status
    url = reverse('cashier:order-by-status', kwargs={'status': 'paid'})
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['page_obj'].paginator.count == 1

    # Test 'unpaid' status
    url = reverse('cashier:order-by-status', kwargs={'status': 'unpaid'})
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['page_obj'].paginator.count == 1


@pytest.mark.django_db
def test_order_detail_view(client, cashier_user,customer_user):
    client.force_login(cashier_user)

    # Create an order and payments
    order = Order.objects.create(user=customer_user, status='pending')
    payment1 = OrderPayment.objects.create(order=order,authority='232452', amount=100)
    payment2 = OrderPayment.objects.create(order=order,authority='849101', amount=200)

    url = reverse('cashier:order-details', kwargs={'order_id': order.id})
    response = client.get(url)

    assert response.status_code == 200
    assert response.context['order'] == order
    payments = list(response.context['payments'])
    assert payment1 in payments and payment2 in payments

@pytest.mark.django_db
def test_order_detail_view_redirects_if_order_not_found(client, cashier_user,customer_user):
    client.force_login(cashier_user)
    url = reverse('cashier:order-details', kwargs={'order_id': 9999})
    response = client.get(url)
    assert response.status_code == 302  # Redirect
    assert response.url == reverse('cashier:dashboard')


@pytest.mark.django_db
def test_change_order_status_view(client, cashier_user,customer_user,site_info):
    client.force_login(cashier_user)
    order = Order.objects.create(user=customer_user, status='pending')

    url = reverse('cashier:change-order-status', kwargs={'order_id': order.id})
    response = client.post(url, {'status': 'paid'})

    order.refresh_from_db()
    assert order.status == 'paid'
    assert response.status_code == 302
    assert response.url.startswith(reverse('cashier:dashboard'))

@pytest.mark.django_db
def test_change_order_status_view_order_not_found(client, cashier_user,customer_user,site_info):
    client.force_login(cashier_user)
    url = reverse('cashier:change-order-status', kwargs={'order_id': 9999})
    response = client.post(url, {'status': 'paid'})
    assert response.status_code == 302
    assert response.url == reverse('cashier:dashboard')



@pytest.mark.django_db
def test_change_password_view_get(client, cashier_user):
    client.force_login(cashier_user)
    url = reverse('cashier:change-password')
    response = client.get(url)
    assert response.status_code == 200
    assert 'form' in response.context

@pytest.mark.django_db
def test_change_password_view_post_valid(client, cashier_user):
    client.force_login(cashier_user)
    url = reverse('cashier:change-password')
    data = {
        'old_password': 'testpass',
        'new_password1': 'newstrongpass123',
        'new_password2': 'newstrongpass123',
    }
    response = client.post(url, data)
    assert response.status_code == 302
    assert response.url == reverse('cashier:dashboard')
    cashier_user.refresh_from_db()
    assert cashier_user.check_password('newstrongpass123')

@pytest.mark.django_db
def test_change_password_view_post_invalid(client, cashier_user):
    client.force_login(cashier_user)
    url = reverse('cashier:change-password')
    data = {
        'old_password': 'wrongpass',
        'new_password1': 'short',
        'new_password2': 'short',
    }
    response = client.post(url, data)
    assert response.status_code == 200
    assert 'form' in response.context
    assert response.context['form'].errors