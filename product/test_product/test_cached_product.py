import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sufficient.settings")
import django
django.setup()
import pytest
import product.cache.cached_product as cached_product
from product.models import Banner, AboutProduct, AboutAfterBeforeProduct, CountDownBanner, Brands, Product
from product.test_product.test_product_fixture import *


@pytest.mark.django_db
def test_get_banner_cache(banner):
    result = cached_product.get_banner()
    banners = list(Banner.objects.all().order_by('order'))
    assert list(result) == banners

@pytest.mark.django_db
def test_get_about_product_cache( about_product):
    result = cached_product.get_about_product()
    about_products = list(AboutProduct.objects.all().order_by('order'))
    assert list(result) == about_products

@pytest.mark.django_db
def test_get_countDownBanner_cache(countdown_banner):
    result = cached_product.get_countDownBanner()
    countdown = CountDownBanner.objects.filter().first()
    assert result == countdown

@pytest.mark.django_db
def test_get_AfterBeforeProduct_cache(about_after_before_product):
    result = cached_product.get_AfterBeforeProduct()
    after_before = AboutAfterBeforeProduct.objects.first()
    assert result == after_before

@pytest.mark.django_db
def test_get_brands_cache( brand):
    result = cached_product.get_brands()
    brands = list(Brands.objects.all().order_by('order'))
    assert list(result) == brands

# @pytest.mark.django_db
# def test_get_home_products_cache(product):
#     result = cached_product.get_home_products()
#     products = list(Product.objects.filter().order_by('order'))
#     assert list(result) == products