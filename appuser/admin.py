from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from django.contrib.auth.models import Group
from jalali_date import datetime2jalali
from jalali_date.admin import ModelAdminJalaliMixin
from appuser.apps import AppuserConfig
from appuser.models import *
from eshop.custom_admin import custom_admin_site


# Register your models here.
# class AddressInline(admin.StackedInline):
#     model = Address
#     can_delete = False


class AppUserAdmin(ModelAdminJalaliMixin, ModelAdmin):
    model = AppUser
    list_display = ('username', 'get_full_name')
    list_filter = ('groups',)
    search_fields = ('email', 'first_name', 'last_name','username')
    ordering = ('username',)



class VerificationUserAdmin(ModelAdminJalaliMixin,ModelAdmin):
    model = VerificationUser
    list_display = ('username', 'verification_code','valid_until_jalali')
    search_fields = ('username', 'verification_code' )
    ordering = ('username',)

    def valid_until_jalali(self, obj):
        return datetime2jalali(obj.valid_until).strftime('%Y/%m/%d  %H:%M:%S')
    valid_until_jalali.short_description = 'اعتبار کد تایید'

class PageVisitedAdmin(ModelAdminJalaliMixin,ModelAdmin):
    model = PageVisit
    list_display = ('user__username','ip_address','getVisited_PersainDate')
    search_fields = ('user__username', 'ip_address', 'page_url','visited_at')
    ordering = ('-visited_at',)


custom_admin_site.register(AppUser,AppUserAdmin)
custom_admin_site.register(VerificationUser,VerificationUserAdmin)
custom_admin_site.register(PageVisit,PageVisitedAdmin)
custom_admin_site.register(Group)