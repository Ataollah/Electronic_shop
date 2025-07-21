import pytest
from product.test_product.test_product_fixture import *
from product.templatetags import product_tags
from product.models import Banner, AboutProduct, AboutAfterBeforeProduct, CountDownBanner, Brands, Product

@pytest.mark.django_db
def test_show_banner_returns_banners(banner):
    context = product_tags.show_banner()
    banners = list(Banner.objects.all().order_by('order'))
    assert context['banners'][0].small_title == banners[0].small_title

@pytest.mark.django_db
def test_show_about_product_returns_about_products(about_product):
    context = product_tags.show_about_product()
    about_products = list(AboutProduct.objects.all().order_by('order'))
    assert context['about_products'][0].title == about_products[0].title

@pytest.mark.django_db
def test_show_count_down_banner_returns_item(countdown_banner):
    context = product_tags.show_count_down_banner()
    item = CountDownBanner.objects.first()
    assert context['item'].title == item.title


@pytest.mark.django_db
def test_show_brands_returns_brands(brand):
    context = product_tags.show_brands()
    brands = list(Brands.objects.all().order_by('order'))
    assert context['brands'][0].title == brands[0].title

