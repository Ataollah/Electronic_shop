import pytest
from django.urls import reverse
from product.test_product.test_product_fixture import *

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