import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from unittest.mock import patch

@pytest.mark.django_db
def test_send_code_post():
    client = APIClient()
    url = reverse('send-code-api')  # Make sure your urls.py has name='send-code' for SendCode
    data = {'username': '09111111111'}
    with patch('appuser.views.api_views.VerificationMessageSender') as mock_sender:
        instance = mock_sender.return_value
        response = client.post(url, data, format='json')
        assert response.status_code == 200
        instance.sendCode.assert_called_once()


@pytest.mark.django_db
def test_send_code_to_candid_user_post():
    client = APIClient()
    url = reverse('send-code-to-candid-api')  # Make sure your urls.py has name='send-code-to-candid-user' for SendCodeToCandidUser
    data = {'username': '09111111111'}
    with patch('appuser.views.api_views.VerificationMessageSender') as mock_sender:
        instance = mock_sender.return_value
        with patch('appuser.views.api_views.AppUser.objects.filter') as mock_filter:
            mock_filter.return_value.exists.return_value = False  # Simulate user does not exist
            response = client.post(url, data, format='json')
            assert response.status_code == 200
            instance.sendCode.assert_called_once()

@pytest.mark.django_db
def test_send_code_to_candid_user_post_user_exists():
    client = APIClient()
    url = reverse('send-code-to-candid-api')
    data = {'username': '09111111111'}
    with patch('appuser.views.api_views.VerificationMessageSender') as mock_sender:
        with patch('appuser.views.api_views.AppUser.objects.filter') as mock_filter:
            mock_filter.return_value.exists.return_value = True  # Simulate user exists
            response = client.post(url, data, format='json')
            assert response.status_code == 400

@pytest.mark.django_db
def test_send_code_to_user_post_user_exists():
    client = APIClient()
    url = reverse('send-code-to-user-api')  # Make sure your urls.py has name='send-code-to-user' for SendCodeToUser
    data = {'username': '09111111111'}
    with patch('appuser.views.api_views.VerificationMessageSender') as mock_sender:
        instance = mock_sender.return_value
        with patch('appuser.views.api_views.AppUser.objects.filter') as mock_filter:
            mock_filter.return_value.exists.return_value = True  # Simulate user exists
            response = client.post(url, data, format='json')
            assert response.status_code == 200
            instance.sendCode.assert_called_once()

@pytest.mark.django_db
def test_send_code_to_user_post_user_not_exists():
    client = APIClient()
    url = reverse('send-code-to-user-api')
    data = {'username': '09111111111'}
    with patch('appuser.views.api_views.VerificationMessageSender') as mock_sender:
        with patch('appuser.views.api_views.AppUser.objects.filter') as mock_filter:
            mock_filter.return_value.exists.return_value = False  # Simulate user does not exist
            response = client.post(url, data, format='json')
            assert response.status_code == 400
