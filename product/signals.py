from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache

from blog.models import PostList
from product.models import Product, Banner, AboutProduct, CountDownBanner, AboutAfterBeforeProduct, Brands, SpecialList, \
    SpecialListItem


@receiver(post_save, sender=Product)
@receiver(post_delete, sender=Product)
def invalidate_product_cache(sender, **kwargs):
    cache.delete('home_products')

@receiver(post_save, sender=Banner)
@receiver(post_delete, sender=Banner)
def invalidate_banner_cache(sender, **kwargs):
    cache.delete('banner')

@receiver(post_save, sender=AboutProduct)
@receiver(post_delete, sender=AboutProduct)
def invalidate_about_product_cache(sender, **kwargs):
    cache.delete('about_product')


@receiver(post_save, sender=CountDownBanner)
@receiver(post_delete, sender=CountDownBanner)
def invalidate_count_down_banner_cache(sender, **kwargs):
    cache.delete('countDownBanner')

@receiver(post_save, sender=AboutAfterBeforeProduct)
@receiver(post_delete, sender=AboutAfterBeforeProduct)
def invalidate_after_before_product_cache(sender, **kwargs):
    cache.delete('after_before_product')


@receiver(post_save, sender=Brands)
@receiver(post_delete, sender=Brands)
def invalidate_brands_cache(sender, **kwargs):
    cache.delete('brands')


@receiver(post_save, sender=Product)
@receiver(post_delete, sender=Product)
@receiver(post_save, sender=SpecialList)
@receiver(post_delete, sender=SpecialList)
@receiver(post_save, sender=SpecialListItem)
@receiver(post_delete, sender=SpecialListItem)
def invalidate_featured_products_cache(sender, **kwargs):
    cache.delete('featured_products')
    print('featured_products invalidated')








