# siteInfo/signals.py
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from siteInfo.models import Menu, SiteInfo, Links, SocialMedia, SubMenu, Gallery, Testimonial


@receiver(post_save, sender=Menu)
@receiver(post_delete, sender=Menu)
@receiver(post_save, sender=SubMenu)
@receiver(post_delete, sender=SubMenu)
def invalidate_menu_cache(sender, **kwargs):
    cache.delete('menu')

@receiver(post_save, sender=SiteInfo)
@receiver(post_delete, sender=SiteInfo)
def invalidate_site_info_cache(sender, **kwargs):
    cache.delete('siteInfo')

@receiver(post_save, sender=Links)
@receiver(post_delete, sender=Links)
def invalidate_links_cache(sender, **kwargs):
    cache.delete('internal')
    cache.delete('external')

@receiver(post_save, sender=SocialMedia)
@receiver(post_delete, sender=SocialMedia)
def invalidate_social_media_cache(sender, **kwargs):
    cache.delete('social_media')

@receiver(post_save, sender=Gallery)
@receiver(post_delete, sender=Gallery)
def invalidate_gallery_cache(sender, **kwargs):
    cache.delete('gallery')

@receiver(post_save, sender=Testimonial)
@receiver(post_delete, sender=Testimonial)
def invalidate_testimonial_cache(sender, **kwargs):
    cache.delete('testimonial')

