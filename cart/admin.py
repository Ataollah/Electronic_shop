import jdatetime
from django.contrib import admin

from cart.models import CartItem, Cart
from eshop.custom_admin import custom_admin_site


# Register your models here.

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0

class CartAdmin(admin.ModelAdmin):
    model = Cart
    list_display = ('user', 'getPersianCreatedAt')
    list_filter = ('user', 'created_at')
    search_fields = ('user__username','user__first_name','user__last_name','items__product__title', 'created_at')
    ordering = ('-created_at',)
    inlines = (CartItemInline,)


    def get_search_results(self, request, queryset, search_term):
        # Default search
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        # Try to parse search_term as Jalali date
        try:
            jalali_date = jdatetime.datetime.strptime(search_term, '%Y/%m/%d')
            gregorian_start = jalali_date.togregorian()
            gregorian_end = (jalali_date.replace(hour=23, minute=59, second=59)).togregorian()
            queryset |= self.model.objects.filter(
                created_at__range=(gregorian_start, gregorian_end)
            )
        except (ValueError, TypeError):
            pass
        return queryset, use_distinct



custom_admin_site.register(Cart, CartAdmin)
