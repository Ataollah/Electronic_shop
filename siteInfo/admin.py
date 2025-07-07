from django.contrib import admin
from django.contrib.sites.models import Site
from eshop.custom_admin import custom_admin_site
from siteInfo.models import Menu, SMSProvider, SubMenu, SiteInfo, SocialMedia, Links, FAQ, Gallery, Testimonial, \
    MailProvider


# Register your models here.

class SubMenuInLine(admin.TabularInline):
    model = SubMenu
    extra = 1


class MenuAdmin(admin.ModelAdmin):
    model = Menu
    list_display = ('name', 'url')
    ordering = ('order', 'name')
    search_fields = ('name', 'url', 'order')
    inlines = [SubMenuInLine]


class WebSiteInfoAdmin(admin.ModelAdmin):
    model = SiteInfo
    list_display = ('name',)


class SocialMediaAdmin(admin.ModelAdmin):
    model = SocialMedia
    search_fields = ('type', 'url')
    list_display = ('type', 'url')


class LinksAdmin(admin.ModelAdmin):
    model = Links
    list_display = ('title', 'url', )
    search_fields = ('title', 'url',)


class FAQAdmin(admin.ModelAdmin):
    model = FAQ
    list_display = ('question',)
    search_fields = ('question', 'answer')
    ordering = ('question',)


class GalleryAdmin(admin.ModelAdmin):
    model = Gallery
    list_display = ('title',)
    ordering = ('title',)


class SMSProviderAdmin(admin.ModelAdmin):
    model = SMSProvider
    list_display = ('name',)
    ordering = ('name',)
    search_fields = ('name', 'api_key', 'api_secret')

class MailProviderAdmin(admin.ModelAdmin):
    model = MailProvider
    list_display = ('name',)
    ordering = ('name',)

class TestimonialAdmin(admin.ModelAdmin):
    model = Testimonial
    list_display = ('name', 'message')
    search_fields = ('name', 'message')
    ordering = ('name',)


custom_admin_site.register(Menu, MenuAdmin)
custom_admin_site.register(SiteInfo, WebSiteInfoAdmin)
custom_admin_site.register(SocialMedia, SocialMediaAdmin)
custom_admin_site.register(Links, LinksAdmin)
custom_admin_site.register(FAQ, FAQAdmin)
custom_admin_site.register(Gallery, GalleryAdmin)
custom_admin_site.register(SMSProvider, SMSProviderAdmin)
custom_admin_site.register(Testimonial, TestimonialAdmin)
custom_admin_site.register(MailProvider, MailProviderAdmin)
custom_admin_site.register(Site)
