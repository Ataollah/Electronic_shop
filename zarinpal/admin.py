from django.contrib import admin
from eshop.custom_admin import custom_admin_site
from zarinpal.models import ZarinPal


# Register your models here.

class ZarinPalAdmin(admin.ModelAdmin):
    model = ZarinPal
    list_display = ('id', 'merchant_id', 'sandbox')
    search_fields = ('merchant_id', 'sandbox')


custom_admin_site.register(ZarinPal, ZarinPalAdmin)
