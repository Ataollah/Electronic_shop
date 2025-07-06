from django import template
from siteInfo.cache.site_info_cache import getMenu, getSiteInfo, getLink, getSocialMedia, getGallery, getBannerData, \
    getTestimonial, getMainPagePosts

register = template.Library()


@register.inclusion_tag('Layout/Base/Components/TopHeader/top_header.html')
def top_header():
    siteInfo = getSiteInfo()
    social_media = getSocialMedia()
    return {'siteInfo': siteInfo, 'social_media': social_media}


@register.inclusion_tag('Layout/Base/Components/Header/header.html', takes_context=True)
def header(context):
    request = context.get('request')
    menus = getMenu()
    print(menus)
    siteInfo = getSiteInfo()
    social_media = getSocialMedia()
    return {'menus': menus, 'social_media': social_media,
            'request': request, 'siteInfo': siteInfo, 'user': request.user}


@register.inclusion_tag('Layout/Base/Components/Footer/footer.html')
def footer(sub_form=None):
    siteInfo = getSiteInfo()
    links = getLink()
    social_media = getSocialMedia()
    return {'siteInfo': siteInfo, 'links': links
        , 'social_media': social_media,
            'sub_form': sub_form}


@register.inclusion_tag('Pages/Home/Components/Testimonial/testimonials.html')
def show_testimonial():
    testimonials = getTestimonial()
    return {'testimonials': testimonials}


@register.inclusion_tag('Pages/Home/Components/Instagram/instagram.html')
def show_instagram():
    gallery = getGallery()
    siteInfo = getSiteInfo()
    return {'gallery': gallery, 'siteInfo': siteInfo}


@register.inclusion_tag('Pages/Home/Components/Blog/blogs.html')
def show_posts():
    posts = getMainPagePosts()
    print('main page posts : ', posts)
    for post in posts:
        print(post)
    return {'posts': posts}


@register.simple_tag
def getEnamadID():
    siteInfo = getSiteInfo()
    if siteInfo:
        return siteInfo.enamad_id
    return ''


@register.simple_tag(takes_context=True)
def query_transform(context, page_number):
    request = context['request']
    print("request.GET : ")
    strUrl = '?'
    for key in request.GET.keys():
        if key == 'page':
            print('page found')
            continue
        values = request.GET.getlist(key)
        for value in values:
            strUrl += f"{key}={value}&"
    strUrl += "page=" + str(page_number)
    print(strUrl)
    return strUrl


@register.simple_tag(takes_context=True)
def print_querystring(context):
    request = context['request']
    print("request.GET : ")
    strUrl = '?'
    for key in request.GET.keys():
        if key == 'page': continue
        values = request.GET.getlist(key)
        for value in values:
            strUrl += f"{key}={value}&"

    print(strUrl)
    return ''


@register.filter(name='get_media')
def get_media(value, arg):
    if hasattr(value, 'filter'):
        return value.filter(type=arg).first()
    return None


@register.filter
def range_filter(value):
    return range(value)


@register.filter
def uncheckedStar(value):
    return range(5 - value)
