from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.conf import settings
from Utility.orphan_file_cleaner import update_file_field, delete_file_field
from product.models import Product


class Order(models.Model):
    ORDER_STATUS = [
        ('unpaid', 'پرداخت نشده'),
        ('paid', 'پرداخت شده'),
        ('pending', 'در حال پردازش'),
        ('delivered', 'تحویل داده شده'),
        ('canceled', 'انصراف'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders', verbose_name='کاربر')
    total_amount = models.BigIntegerField(default=0, verbose_name='مبلغ به ریال')
    discount = models.BigIntegerField(default=0, verbose_name='تخفیف به ریال')
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default='unpaid', verbose_name='وضعیت')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ و ساعت ایجاد ')
    updated_at =  models.DateTimeField(auto_now=True, verbose_name='تاریخ و ساعت بروزرسانی ')
    description = models.TextField(verbose_name='توضیحات',null=True, blank=True)
    province = models.CharField(max_length=100, default='تهران', verbose_name='استان')
    county = models.CharField(max_length=100, default='تهران', verbose_name='شهرستان')
    district = models.CharField(max_length=100, default='مرکزی', verbose_name='منطقه')
    city = models.CharField(max_length=100, default='تهران', verbose_name='شهر')
    rural = models.CharField(max_length=100, blank=True, null=True, verbose_name='روستا')
    address = models.TextField(blank=True, null=True, verbose_name='آدرس')
    postal_code = models.CharField(max_length=10, verbose_name='کد پستی', blank=True, null=True)

    def get_persian_status(self):
        order_dict = dict(self.ORDER_STATUS)
        print('persian status : ',order_dict['delivered'])
        return order_dict.get(self.status)
    get_persian_status.short_description = 'وضعیت سفارش فارسی'

    def get_full_address(self):
        return f"استان : {self.province} - شهرستان : {self.county} - منطقه : {self.district} - شهر :  {self.city} - روستا : {self.rural} <br>  خیابان : {self.address} <br> کدپستی :  {self.postal_code}"
    get_full_address.short_description = 'آدرس کامل'


    def save(self, *args, **kwargs):
        # Get previous status if the object exists
        if self.pk:
            prev = Order.objects.get(pk=self.pk)
            if prev.status != 'canceled' and self.status == 'canceled':
                for item in self.items.select_related('product').all():
                    item.product.inventory += item.quantity
                    item.product.save()
        super().save(*args, **kwargs)


    class Meta:
        verbose_name = 'سفارش'
        verbose_name_plural = 'سفارشات'

    def __str__(self):
        return f"سفارش شماره  {self.id} توسط {self.user.username}"

class OrderItems(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name='سفارش')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='ordered_products', verbose_name='محصول')
    quantity = models.PositiveIntegerField(default=1, verbose_name='تعداد')
    price = models.BigIntegerField(default=0, verbose_name='مبلغ')

    class Meta:
        verbose_name = 'کالای سفارش'
        verbose_name_plural = 'کالاهای سفارش'

    def total_price(self):
        return self.price * self.quantity

    def __str__(self):
        return f"Order Item {self.product.title} in Order {self.order.id}"

class OrderPayment(models.Model):
    PAYMENT_STATUS = [
        ('paid', 'پرداخت شده'),
        ('failed', 'ناموفق'),
    ]
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payments', verbose_name='سفارش')
    amount = models.BigIntegerField(default=0, verbose_name='مبلغ ')
    transaction_id = models.CharField(default='111111',max_length=200, verbose_name='شماره تراکنش')
    authority = models.CharField(default='auth-222222',unique=True,max_length=200, verbose_name='شناسه زرین پال')
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='failed', verbose_name='وضعیت')
    created_at =  models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at =  models.DateTimeField(auto_now_add=True, verbose_name='تاریخ بروز رسانی')

    def getStatus(self):
        payment_dict = dict(self.PAYMENT_STATUS)
        return payment_dict.get(self.status)
    getStatus.short_description = 'وضعیت پرداخت'

    def get_status_persian(self):
        status_dict = {
            'paid': 'پرداخت شده',
            'failed': 'ناموفق',
        }
        return status_dict.get(self.status, 'نامشخص')

    class Meta:
        verbose_name = 'پرداخت  سفارش'
        verbose_name_plural = 'پرداخت های  سفارش'

    def __str__(self):
        return f"پرداخت شماره{self.id} برای سفارش شماره {self.order.id}"

