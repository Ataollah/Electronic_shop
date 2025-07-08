from django.contrib import admin
from eshop import custom_admin
from eshop.custom_admin import custom_admin_site
from supplier.models import Supplier, Salesman, SocialMedia


# Register your models here.


class SupplierAdmin(admin.ModelAdmin):
    model = Supplier
    list_display = ('name', 'email', 'phone1', 'phone2', 'website', 'address', 'created_at')
    search_fields = ('name', 'email', 'phone1', 'phone2', 'website')
    list_filter = ('created_at',)


class SocialMediaInline(admin.TabularInline):
    model = SocialMedia
    extra = 1


class SalesmanAdmin(admin.ModelAdmin):
    model = Salesman
    list_display = ('name', 'email', 'phone', 'supplier')
    search_fields = ('name', 'email', 'phone', 'supplier__name')
    list_filter = ('supplier',)
    inlines = [SocialMediaInline]


custom_admin_site.register(Supplier, SupplierAdmin)
custom_admin_site.register(Salesman, SalesmanAdmin)
