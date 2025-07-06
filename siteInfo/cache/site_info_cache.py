from django.core.cache import cache
from siteInfo.models import Links, SocialMedia
import os
from dotenv import load_dotenv


load_dotenv()

SHORT_CACHE_TIME = int(os.getenv('SHORT_CACHE_TIME', 0))
MID_CACHE_TIME = int(os.getenv('MID_CACHE_TIME', 0))
LONG_CACHE_TIME = int(os.getenv('LONG_CACHE_TIME', 0))
DEBUG_CACHE_TIME = int(os.getenv('DEBUG_CACHE_TIME', 0))



def getMenu():
    result = cache.get('menu')
    if not result:
        from siteInfo.models import Menu
        result = Menu.objects.all().order_by('order')
        cache.set('menu', result, DEBUG_CACHE_TIME)
    return result

def getGallery():
    result = cache.get('gallery')
    if not result:
        from siteInfo.models import Gallery
        result = Gallery.objects.all()
        cache.set('gallery', result, DEBUG_CACHE_TIME)
    return result

def getBannerData():
    result = cache.get('banner_data')
    if not result:
        from blog.models import Post
        result = Post.objects.filter(page_type__exact='banner').first()
        cache.set('banner_data', result, DEBUG_CACHE_TIME)
    return result

# def getCategories():
#     result = cache.get('categories')
#     if not result:
#         result = MainCategory.objects.prefetch_related('subcategories__childcategories').all().order_by('order')
#         cache.set('categories', result, DEBUG_CACHE_TIME)
#     return result

def getSiteInfo():
    result = cache.get('siteInfo')
    if not result:
        from siteInfo.models import SiteInfo
        result = SiteInfo.objects.first()
        cache.set('siteInfo', result, DEBUG_CACHE_TIME)
    return result

def getLink():
    result = cache.get('links')
    if not result:
        result = Links.objects.all()
        cache.set('links', result, DEBUG_CACHE_TIME)
    return result

def getSocialMedia():
    result = cache.get('social_media')
    if not result:
        result = SocialMedia.objects.all()
        cache.set('social_media', result, DEBUG_CACHE_TIME)
    return result

def getTestimonial():
    result = cache.get('testimonial')
    if not result:
        from siteInfo.models import Testimonial
        result = Testimonial.objects.all().order_by('order')
        cache.set('testimonial', result, DEBUG_CACHE_TIME)
    return result

def getMainPagePosts():
    result = cache.get('main_page_blogs')
    if not result:
        from blog.models import PostList,Post
        post_ids = PostList.objects.filter(place='main_page').values_list('posts', flat=True)
        result = Post.objects.prefetch_related('media').filter(id__in=post_ids).order_by('publishedAt')
        cache.set('main_page_blogs', result, DEBUG_CACHE_TIME)
    return result



