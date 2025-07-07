from django.contrib import admin

from newsletter.models import Subscriber
from eshop import custom_admin
from eshop.custom_admin import custom_admin_site


# Register your models here.

class SubscriberAdmin(admin.ModelAdmin):
    model = Subscriber
    list_display = ('email', 'getPersianSubscribedAt')
    search_fields = ('email',)
    ordering = ('-subscribed_at',)


custom_admin_site.register(Subscriber, SubscriberAdmin)
