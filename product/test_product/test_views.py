import pytest
from django.urls import reverse
from product.test_product.test_product_fixture import *
from appuser.tests.appuser_fixtures import customer_user,app_user
from product.models import PriceInquiryRequest

@pytest.mark.django_db
def test_shop_list_view(client,category,product):
    url = reverse('shop-view')  # Replace with your actual url name
    response = client.get(url)
    assert response.status_code == 200
    assert 'products' in response.context
    assert product in response.context['products']
    assert 'categories' in response.context
    assert category in response.context['categories']


@pytest.mark.django_db
def test_product_detail_view(client,category,product):

    # Add related products
    for i in range(5):
        Product.objects.create(title=f"Related {i}",primary_image=create_product_image(),secondary_image=create_product_image(), category=category, current_price=5+i, slug=f"related-{i}")

    url = reverse('product-detail-view', kwargs={'slug': product.slug})  # Replace with your url name
    response = client.get(url)
    assert response.status_code == 200
    assert 'related_products' in response.context
    assert all(p.category == category and p.id != product.id for p in response.context['related_products'])
    assert 'siteInfo' in response.context
    assert 'questions' in response.context


@pytest.mark.django_db
def test_price_inquiry_already_exists(client, customer_user, product):
    client.force_login(customer_user)
    PriceInquiryRequest.objects.create(user=customer_user, product=product, status='waiting')
    url = reverse('price-inquiry-view')  # Replace with your url name
    response = client.post(url, {'product_id': product.id})
    assert response.status_code == 200
    assert 'product/InquiryExisted/already_existed.html' in [t.name for t in response.templates]
    assert PriceInquiryRequest.objects.filter(user=customer_user, product=product, status='waiting').count() == 1

@pytest.mark.django_db
def test_price_inquiry_create_success(client, customer_user, product):
    client.force_login(customer_user)
    url = reverse('price-inquiry-view')  # Replace with your url name
    response = client.post(url, {'product_id': product.id})
    assert response.status_code == 200
    print(response.templates)
    assert 'product/InquirySuccess/inquiry_success.html' in [t.name for t in response.templates]
    assert PriceInquiryRequest.objects.filter(user=customer_user, product=product, status='waiting').count() == 1