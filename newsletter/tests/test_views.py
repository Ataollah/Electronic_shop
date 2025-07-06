import pytest
from django.urls import reverse

@pytest.mark.django_db
def test_subscribe_success_view_renders_template(client):
    url = reverse('newsletter:success')  # Adjust if your URL name differs
    response = client.get(url)
    assert response.status_code == 200
    assert 'با موفقیت در خبرنامه ثبت شد'.encode('utf-8') in response.content  # Adjust if your template contains this text