import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from django.test import Client
from unittest.mock import patch
from appuser.tests.appuser_fixtures import *

@pytest.mark.django_db
def test_login_view_get():
    client = Client()
    url = reverse('login-view')  # Make sure your urls.py has a name='login' for LoginView
    response = client.get(url)
    assert response.status_code == 200
    assert 'form' in response.context

@pytest.mark.django_db
def test_login_view_post_valid(app_user):
    client = Client()
    user = app_user
    url = reverse('login-view')
    data = {'username': '09111111111', 'password': 'testpass'}
    with patch('appuser.views.views.authenticate') as mock_auth:
        mock_auth.return_value = user
        response = client.post(url, data)
        assert response.status_code == 302  # Adjust if you redirect after login
        mock_auth.assert_called_once_with(response.wsgi_request, username='09111111111', password='testpass')

@pytest.mark.django_db
def test_login_view_post_invalid():
    client = Client()
    url = reverse('login-view')
    data = {'username': 'wrong', 'password': 'wrong'}
    with patch('django.contrib.auth.authenticate') as mock_auth:
        mock_auth.return_value = None
        response = client.post(url, data)
        assert response.status_code == 200
        assert 'form' in response.context

@pytest.mark.django_db
def test_logout_view(client, app_user):
    client.login(username=app_user.username, password="testpass")
    # Ensure user is authenticated
    response = client.get(reverse('login-view'))
    assert response.wsgi_request.user.is_authenticated
    # Call logout view
    response = client.get(reverse('logout-view'))
    # Should redirect to login page
    assert response.status_code == 302
    assert response.url == reverse('login-view')
    # User should be logged out
    response = client.get(reverse('login-view'))
    assert not response.wsgi_request.user.is_authenticated

@pytest.mark.django_db
def test_candid_phone_verification_view_get(client):
    url = reverse('candid-phone-verification-view')
    response = client.get(url)
    assert response.status_code == 200
    assert 'form' in response.context

@pytest.mark.django_db
def test_candid_phone_verification_view_post_valid(client):
    url = reverse('candid-phone-verification-view')
    data = {'username': '09111111111'}
    with patch('appuser.views.views.VerificationMessageSender') as mock_sender:
        instance = mock_sender.return_value
        response = client.post(url, data)
        # Should redirect to verify-candid-code-view
        assert response.status_code == 302
        assert response.url == reverse('verify-candid-code-view')
        # Should call sendCode
        instance.sendCode.assert_called_once()
        # Session should have candid_username
        assert client.session['candid_username'] == '09111111111'

@pytest.mark.django_db
def test_candid_phone_verification_view_post_invalid(client):
    url = reverse('candid-phone-verification-view')
    data = {'username': ''}  # Invalid, empty username
    response = client.post(url, data)
    assert response.status_code == 200
    assert 'form' in response.context
    assert response.context['form'].errors

@pytest.mark.django_db
def test_user_phone_verification_view_get(client):
    url = reverse('user-phone-verification-view')
    response = client.get(url)
    assert response.status_code == 200
    assert 'form' in response.context

@pytest.mark.django_db
def test_user_phone_verification_view_post_valid(client,app_user):
    url = reverse('user-phone-verification-view')
    data = {'username': '09111111111'}
    with patch('appuser.views.views.VerificationMessageSender') as mock_sender:
        instance = mock_sender.return_value
        response = client.post(url, data)
        assert response.status_code == 302
        assert response.url == reverse('verify-user-code-view')
        instance.sendCode.assert_called_once()
        assert client.session['username'] == '09111111111'

@pytest.mark.django_db
def test_user_phone_verification_view_post_invalid(client):
    url = reverse('user-phone-verification-view')
    data = {'username': ''}  # Invalid, empty username
    response = client.post(url, data)
    assert response.status_code == 200
    assert 'form' in response.context
    assert response.context['form'].errors

@pytest.mark.django_db
def test_verify_candid_code_view_get_with_session(client):
    session = client.session
    session['candid_username'] = '09123456789'
    session.save()
    url = reverse('verify-candid-code-view')
    response = client.get(url)
    assert response.status_code == 200
    assert 'form' in response.context
    assert response.context['username'] == '09123456789'

@pytest.mark.django_db
def test_verify_candid_code_view_get_without_session(client):
    url = reverse('verify-candid-code-view')
    response = client.get(url)
    # Should redirect to 'home' if no candid_username in session
    assert response.status_code == 302
    assert response.url == reverse('home')

@pytest.mark.django_db
def test_verify_candid_code_view_post_valid(client):
    session = client.session
    session['candid_username'] = '09123456789'
    session.save()
    url = reverse('verify-candid-code-view')
    with patch('appuser.views.views.VerifyCodeForm', autospec=True) as mock_form:
        instance = mock_form.return_value
        instance.is_valid.return_value = True
        response = client.post(url, {'code': '123456'})
        assert response.status_code == 302
        assert response.url == reverse('create-user-view')

@pytest.mark.django_db
def test_verify_candid_code_view_post_invalid(client):
    session = client.session
    session['candid_username'] = '09123456789'
    session.save()
    url = reverse('verify-candid-code-view')
    with patch('appuser.views.views.VerifyCodeForm', autospec=True) as mock_form:
        instance = mock_form.return_value
        instance.is_valid.return_value = False
        response = client.post(url, {'code': 'wrong'})
        assert response.status_code == 200
        assert 'form' in response.context
        assert response.context['username'] == '09123456789'

@pytest.mark.django_db
def test_verify_user_code_view_get_with_session(client):
    session = client.session
    session['username'] = '09123456789'
    session.save()
    url = reverse('verify-user-code-view')
    response = client.get(url)
    assert response.status_code == 200
    assert 'form' in response.context
    assert response.context['username'] == '09123456789'

@pytest.mark.django_db
def test_verify_user_code_view_get_without_session(client):
    url = reverse('verify-user-code-view')
    response = client.get(url)
    # Should redirect to 'home' if no username in session
    assert response.status_code == 302
    assert response.url == reverse('home')

@pytest.mark.django_db
def test_verify_user_code_view_post_valid(client):
    session = client.session
    session['username'] = '09123456789'
    session.save()
    url = reverse('verify-user-code-view')
    with patch('appuser.views.views.VerifyCodeForm', autospec=True) as mock_form:
        instance = mock_form.return_value
        instance.is_valid.return_value = True
        response = client.post(url, {'code': '123456'})
        assert response.status_code == 302
        assert response.url == reverse('reset-password-view')

@pytest.mark.django_db
def test_verify_user_code_view_post_invalid(client):
    session = client.session
    session['username'] = '09123456789'
    session.save()
    url = reverse('verify-user-code-view')
    with patch('appuser.views.views.VerifyCodeForm', autospec=True) as mock_form:
        instance = mock_form.return_value
        instance.is_valid.return_value = False
        response = client.post(url, {'code': 'wrong'})
        assert response.status_code == 200
        assert 'form' in response.context
        assert response.context['username'] == '09123456789'

@pytest.mark.django_db
def test_create_user_view_get_with_session(client, mocker):
    session = client.session
    session['candid_username'] = '09123456789'
    session.save()
    url = reverse('create-user-view')
    # Mock Province.objects.all
    mocker.patch('appuser.views.views.Province.objects.all', return_value=[])
    response = client.get(url)
    assert response.status_code == 200
    assert 'form' in response.context
    assert 'provinces' in response.context

@pytest.mark.django_db
def test_create_user_view_get_without_session(client):
    url = reverse('create-user-view')
    response = client.get(url)
    assert response.status_code == 302
    assert response.url == reverse('home')

@pytest.mark.django_db
def test_create_user_view_post_valid(client, mocker):
    session = client.session
    session['candid_username'] = '09123456789'
    session.save()
    url = reverse('create-user-view')
    # Mock Province.objects.all
    mocker.patch('appuser.views.views.Province.objects.all', return_value=[])
    # Mock CreateUserForm
    mock_form = mocker.patch('appuser.views.views.CreateUserForm', autospec=True)
    form_instance = mock_form.return_value
    form_instance.is_valid.return_value = True
    # Mock addToCustomerGroup
    mocker.patch('appuser.views.views.addToCustomerGroup')
    response = client.post(url, {'username': '09123456789'})
    assert response.status_code == 302
    assert response.url == reverse('create-user-succeeded-view')
    form_instance.save.assert_called_once()

@pytest.mark.django_db
def test_create_user_view_post_invalid(client, mocker):
    session = client.session
    session['candid_username'] = '09123456789'
    session.save()
    url = reverse('create-user-view')
    mocker.patch('appuser.views.views.Province.objects.all', return_value=[])
    mock_form = mocker.patch('appuser.views.views.CreateUserForm', autospec=True)
    form_instance = mock_form.return_value
    form_instance.is_valid.return_value = False
    form_instance.errors = {'username': ['This field is required.']}
    response = client.post(url, {'username': ''})
    assert response.status_code == 200
    assert 'form' in response.context
    assert 'provinces' in response.context

@pytest.mark.django_db
def test_created_user_succeeded_view(client):
    session = client.session
    session['candid_username'] = '09123456789'
    session.save()
    url = reverse('create-user-succeeded-view')
    response = client.get(url)
    # Should render the success template
    assert response.status_code == 200
    assert 'candid_username' in response.wsgi_request.session
    assert response.wsgi_request.session['candid_username'] is None
    assert 'appuser/CreateUserSucceeded/create_user_succeeded.html' in [t.name for t in response.templates]

@pytest.mark.django_db
def test_reset_password_view_get_with_session(client, mocker):
    session = client.session
    session['username'] = '09111111111'
    session.save()
    url = reverse('reset-password-view')
    # Mock AppUser.objects.filter().first() to return a user
    mock_user = mocker.Mock()
    mocker.patch('appuser.views.views.AppUser.objects.filter', return_value=mocker.Mock(first=mocker.Mock(return_value=mock_user)))
    mock_form = mocker.patch('appuser.views.views.CustomSetPasswordForm', autospec=True)
    mock_form_instance = mock_form.return_value
    response = client.get(url)
    assert response.status_code == 200
    assert 'form' in response.context

@pytest.mark.django_db
def test_reset_password_view_get_without_session(client):
    url = reverse('reset-password-view')
    response = client.get(url)
    # Should redirect to phone-verification-view if no user
    assert response.status_code == 302
    assert response.url == reverse('user-phone-verification-view')

@pytest.mark.django_db
def test_reset_password_view_post_valid(client, mocker):
    session = client.session
    session['username'] = '09111111111'
    session.save()
    url = reverse('reset-password-view')
    mock_user = mocker.Mock()
    mocker.patch('appuser.views.views.AppUser.objects.filter', return_value=mocker.Mock(first=mocker.Mock(return_value=mock_user)))
    mock_form = mocker.patch('appuser.views.views.CustomSetPasswordForm', autospec=True)
    mock_form_instance = mock_form.return_value
    mock_form_instance.is_valid.return_value = True
    response = client.post(url, {'password1': 'newpass', 'password2': 'newpass'})
    assert response.status_code == 302
    assert response.url == reverse('reset-password-done-view')
    mock_form_instance.save.assert_called_once()

@pytest.mark.django_db
def test_reset_password_view_post_invalid(client, mocker):
    session = client.session
    session['username'] = '09111111111'
    session.save()
    url = reverse('reset-password-view')
    mock_user = mocker.Mock()
    mocker.patch('appuser.views.views.AppUser.objects.filter', return_value=mocker.Mock(first=mocker.Mock(return_value=mock_user)))
    mock_form = mocker.patch('appuser.views.views.CustomSetPasswordForm', autospec=True)
    mock_form_instance = mock_form.return_value
    mock_form_instance.is_valid.return_value = False
    response = client.post(url, {'password1': 'newpass', 'password2': 'wrong'})
    assert response.status_code == 200
    assert 'form' in response.context

@pytest.mark.django_db
def test_reset_password_done_view(client):
    session = client.session
    session['username'] = '09111111111'
    session.save()
    url = reverse('reset-password-done-view')
    response = client.get(url)
    assert response.status_code == 200
    # Session username should be cleared
    assert response.wsgi_request.session['username'] is None
    # Should render the correct template
    assert 'appuser/ResetPassword/reset-pass-done.html' in [t.name for t in response.templates]

