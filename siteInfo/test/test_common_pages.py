import pytest
from django.urls import reverse
from newsletter.models import Subscriber
from blog.models import Post
from blog.tests.blog_fixtures import *
from appuser.tests.appuser_fixtures import *



@pytest.mark.django_db
def test_home_view_get(client):
    url = reverse('home')  # Adjust 'home' to your actual url name
    response = client.get(url)
    assert response.status_code == 200
    assert b'<form' in response.content

@pytest.mark.django_db
def test_home_view_post_valid(client):
    url = reverse('home')
    data = {'email': 'test@example.com'}  # Adjust fields to match SubscriberForm
    response = client.post(url, data)
    assert response.status_code == 302  # Redirect on success
    assert Subscriber.objects.filter(email='test@example.com').exists()

@pytest.mark.django_db
def test_home_view_post_invalid(client):
    url = reverse('home')
    data = {'email': ''}  # Invalid data
    response = client.post(url, data)
    assert response.status_code == 200
    assert b'errorlist' in response.content or b'This field is required' in response.content


@pytest.mark.django_db
def test_about_us_view_get(client,about_us):
    # Create a published post for about_us

    url = reverse('about-us')  # Replace with your actual URL name
    response = client.get(url)
    assert response.status_code == 200
    # Check that the post is in the context (rendered content)
    assert b'About US' in response.content


@pytest.mark.django_db
def test_faq_view_get(client):
    from siteInfo.models import FAQ
    FAQ.objects.create(question='Q1', answer='A1')
    FAQ.objects.create(question='Q2', answer='A2')
    url = reverse('faq')  # Replace 'faq' with your actual URL name
    response = client.get(url)
    assert response.status_code == 200
    assert b'Q1' in response.content
    assert b'Q2' in response.content


@pytest.mark.django_db
def test_contact_us_view_get(client):
    url = reverse('contact-us')  # Replace with your actual URL name
    response = client.get(url)
    assert response.status_code == 200
    assert b'<form' in response.content

@pytest.mark.django_db
def test_contact_us_view_post_valid(client):
    url = reverse('contact-us')
    data = {
        'name': 'Test User',  # Adjust fields to match ContactUSForm
        'subject': 'Test Subject',
        'email': 'test@example.com',
        'message': 'Hello!'
    }
    response = client.post(url, data)
    assert response.status_code == 302  # Redirect on success
    from siteInfo.models import ContactUS
    assert ContactUS.objects.filter(email='test@example.com').exists()

@pytest.mark.django_db
def test_contact_us_view_post_invalid(client):
    url = reverse('contact-us')
    data = {
        'name': '',  # Invalid data
        'subject': '',
        'email': '',
        'message': ''
    }
    response = client.post(url, data)
    assert response.status_code == 200
    print(response.content.decode('utf-8'))
    assert (' <li>این فیلد لازم است.</li>' in response.content.decode() or
            'This field is required' in response.content.decode())


@pytest.mark.django_db
def test_messages_view_displays_and_clears_session(client):
    url = reverse('message-view')  # Replace with your actual URL name
    session = client.session
    session['title'] = 'Test Title'
    session['message'] = 'Test Message'
    session.save()

    response = client.get(url)
    assert response.status_code == 200
    assert b'Test Title' in response.content
    assert b'Test Message' in response.content

    # Check that session variables are cleared
    session = client.session
    assert 'title' not in session
    assert 'message' not in session