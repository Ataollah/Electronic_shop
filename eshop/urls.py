"""
URL configuration for sufficient project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path,include
from blog.BlogSitemap import BlogSiteMap
from product.ProductSitemap import ProductSitemap
from eshop.views import HomeView,PageNotFoundView,PermissionDeniedView
from eshop import settings
from eshop.custom_admin import custom_admin_site
from django.contrib.sitemaps.views import sitemap
from .sitemap import StaticViewSitemap

sitemaps = {
    "static": StaticViewSitemap,
    "blog":BlogSiteMap,
    "product":ProductSitemap,
}


urlpatterns = [
    path("admin/", custom_admin_site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),  # Add this line
    path("", HomeView.as_view(), name="home"),

    path('blog/', include('blog.urls')),
    path('siteInfo/', include('siteInfo.urls')),
    path('appuser/', include('appuser.urls')),
    path('iran/', include('iran.urls')),
    path('product/',include('product.urls')),
    path('cart/', include('cart.urls')),
    path('order/', include('order.urls')),
    path('customer/', include('customer.urls')),
    path('cashier/', include('cashier.urls')),
    path('newsletter/',include('newsletter.urls')),
    path('zarinpal/', include('zarinpal.urls')),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="django.contrib.sitemaps.views.sitemap", )

]

handler403 = PermissionDeniedView.as_view()
handler404 = PageNotFoundView.as_view()

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.conf import settings

    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
