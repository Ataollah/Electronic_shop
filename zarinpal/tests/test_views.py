import pytest
from django.urls import reverse
from unittest.mock import patch
from appuser.tests.appuser_fixtures import cashier_user, customer_user, app_user

@pytest.mark.django_db
def test_send_request_view_redirects_to_zarinpal(client, app_user):
    # Setup: create user, order, and session
    user = app_user
    client.force_login(user)
    from order.models import Order
    order = Order.objects.create(user=user, total_amount=10000)
    session = client.session
    session['order_id'] = order.id
    session.save()

    # Mock Zarinpal API response
    mock_response = {
        'data': {
            'code': 100,
            'authority': 'testauthority'
        }
    }
    with patch('zarinpal.views.requests.post') as mock_post:
        mock_post.return_value.json.return_value = mock_response
        url = reverse('zarinpal:send-request')
        response = client.get(url)
        assert response.status_code == 302
        assert 'zarinpal.com/pg/StartPay/testauthority' in response.url

@pytest.mark.django_db
def test_server_error_view_renders_template(client):
    url = reverse('zarinpal:server-error-view')  # Use your actual URL name
    response = client.get(url)
    assert response.status_code == 200
    assert 'zarinpal/ServerError/server_error.html' in [t.name for t in response.templates]



@pytest.mark.django_db
def test_verify_request_view_success(client, app_user):
    # Setup user, order, and payment
    user = app_user
    from order.models import Order, OrderPayment
    order = Order.objects.create(user=user, total_amount=10000)
    payment = OrderPayment.objects.create(order=order, amount=10000, authority='testauthority')

    # Mock Zarinpal verify API response
    mock_response = {
        'data': {
            'code': 100,
            'ref_id': '123456'
        }
    }
    with patch('zarinpal.views.requests.post') as mock_post:
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = mock_response
        url = reverse('zarinpal:verify-payment')
        response = client.get(url, {'Authority': 'testauthority', 'Status': 'OK'})
        assert response.status_code == 302
        assert response.url == reverse('payment-succeeded-view')

@pytest.mark.django_db
def test_verify_request_view_failure(client, django_user_model):
    user = django_user_model.objects.create_user(username='testuser', email='test@example.com', password='pass')
    from order.models import Order, OrderPayment
    order = Order.objects.create(user=user, total_amount=10000)
    payment = OrderPayment.objects.create(order=order, amount=10000, authority='failauthority')

    url = reverse('zarinpal:verify-payment')
    response = client.get(url, {'Authority': 'failauthority', 'Status': 'NOK'})
    assert response.status_code == 302
    assert response.url == reverse('payment-failed-view')