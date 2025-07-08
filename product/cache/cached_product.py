import os
from datetime import datetime
from django.core.cache import cache
from dotenv import load_dotenv


load_dotenv()

SHORT_CACHE_TIME = int(os.getenv('SHORT_CACHE_TIME', 0))
MID_CACHE_TIME = int(os.getenv('MID_CACHE_TIME', 0))
LONG_CACHE_TIME = int(os.getenv('LONG_CACHE_TIME', 0))
DEBUG_CACHE_TIME = int(os.getenv('DEBUG_CACHE_TIME', 0))


def get_banner():
    result = cache.get('banner')
    if not result:
        from product.models import Banner
        result = Banner.objects.all().order_by('order')
        cache.set('banner', result, DEBUG_CACHE_TIME)
    return result

def get_product_categories():
    result = cache.get('product_categories')
    if not result:
        from product.models import Category
        result = Category.objects.filter(show_on_homepage=True).order_by('order')
        cache.set('product_categories', result, DEBUG_CACHE_TIME)
    return result

def get_about_product():
    result = cache.get('about_product')
    if not result:
        from product.models import AboutProduct
        result = AboutProduct.objects.all().order_by('order')
        cache.set('about_product', result, DEBUG_CACHE_TIME)
    return result


def get_countDownBanner():
    result = cache.get('countDownBanner')
    if not result:
        from product.models import CountDownBanner
        now = datetime.now()
        result = CountDownBanner.objects.filter(end_date__gt=now).first()
        cache.set('countDownBanner', result, DEBUG_CACHE_TIME)
    return result


def get_AfterBeforeProduct():
    result = cache.get('after_before_product')
    if not result:
        from product.models import AboutAfterBeforeProduct
        result = AboutAfterBeforeProduct.objects.first()
        cache.set('after_before_product', result, DEBUG_CACHE_TIME)
    return result

def get_brands():
    result = cache.get('brands')
    if not result:
        from product.models import Brands
        result = Brands.objects.all().order_by('order')
        cache.set('brands', result, DEBUG_CACHE_TIME)
    return result

def get_featured_products():
    result = cache.get('featured_products')
    if not result:
        from product.models import SpecialList
        result = SpecialList.objects.prefetch_related('items').all().order_by('order')
        cache.set('featured_products', result, DEBUG_CACHE_TIME)
    return result