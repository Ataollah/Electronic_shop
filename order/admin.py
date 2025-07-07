import jdatetime
from django.contrib import admin
from order.models import Order, OrderItems, OrderPayment
from eshop.custom_admin import custom_admin_site


# Register your models here.

class OrderItemsAdmin(admin.TabularInline):
    model = OrderItems
    extra = 1
    verbose_name = 'لیست کالا'
    verbose_name_plural = 'لیست کالاها و خدمات سفارش شده'


class OrderPaymentInline(admin.TabularInline):
    model = OrderPayment
    extra = 1
    verbose_name = 'پرداخت  سفارش'
    verbose_name_plural = 'پرداخت های سفارش ها'


class OrderAdmin(admin.ModelAdmin):
    model = Order
    list_display = ('id', 'user', 'status', 'getPersianCreatedAt',)
    list_filter = ('status', 'created_at', )
    search_fields = ('user__username','user__first_name','user__last_name','status','items__product__title')
    ordering = ('-created_at',)
    inlines = (OrderItemsAdmin,OrderPaymentInline,)

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


custom_admin_site.register(Order, OrderAdmin)



