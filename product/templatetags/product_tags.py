from django.utils import timezone
from django import template
from product.cache.cached_product import get_banner

register = template.Library()

@register.inclusion_tag('Pages/Home/Components/Banner/banner.html')
def show_banner():
    banners = get_banner()
    return {'banners': banners}

@register.inclusion_tag('Pages/Home/Components/ProductCategory/product_categories.html')
def show_product_categories():
    from product.cache.cached_product import get_product_categories
    product_categories = get_product_categories()
    return {'categories': product_categories}


@register.inclusion_tag('Pages/Home/Components/AboutProduct/about_product.html')
def show_about_product():
    from product.cache.cached_product import get_about_product
    about_products = get_about_product()
    return {'about_products': about_products}


@register.inclusion_tag('Pages/Home/Components/CountDownBanner/count_down_banner.html')
def show_count_down_banner():
    from product.cache.cached_product import get_countDownBanner
    count_down_banner = get_countDownBanner()
    return {'item': count_down_banner}



@register.inclusion_tag('Pages/Home/Components/Brands/brands.html')
def show_brands():
    from product.cache.cached_product import get_brands
    brands = get_brands()
    return {'brands': brands}


@register.inclusion_tag('Pages/Home/Components/FeaturedProducts/featured_products.html')
def show_featured_products():
    from product.cache.cached_product import get_featured_products
    special_list = get_featured_products()
    return {'special_list': special_list,'current_time':timezone.now()}


