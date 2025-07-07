from django.contrib import admin
from iran.models import *
from eshop import custom_admin
from eshop.custom_admin import custom_admin_site


# Register your models here.


class ProvinceAdmin(admin.ModelAdmin):
    model = Province
    list_display = ('name', 'tel_prefix')
    search_fields = ('name', 'tel_prefix')
    ordering = ('name',)

class CountyAdmin(admin.ModelAdmin):
    model = County
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)

class DistrictAdmin(admin.ModelAdmin):
    model = District
    list_display = ('name', )
    search_fields = ('name', )
    ordering = ('name',)

class RuralAdmin(admin.ModelAdmin):
    model = Rural
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)


custom_admin_site.register(Province, ProvinceAdmin)
custom_admin_site.register(County, CountyAdmin)
custom_admin_site.register(District, DistrictAdmin)
custom_admin_site.register(Rural, RuralAdmin)
