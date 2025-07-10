import pytest
from django.urls import reverse
from django.test import Client
from appuser.tests.appuser_fixtures import app_user,cashier_user

@pytest.mark.django_db
def test_permission_denied_view(cashier_user):
    client = Client()
    client.force_login(cashier_user)
    response = client.get(reverse('price-inquiry-view'))
    assert response.status_code == 403
    assert 'دسترسی غیر مجاز'.encode('utf-8') in response.content

@pytest.mark.django_db
def test_page_not_found_view():
    client = Client()
    response = client.get('/nonexistent-page/')
    assert response.status_code == 404
    assert 'صفحه ناموجود'.encode('utf-8') in response.content
