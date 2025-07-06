from celery.backends.database import retry
from django.db import models
from django.utils import timezone
from datetime import timedelta
from product.models import Product


class Cart(models.Model):
    user = models.OneToOneField('appuser.AppUser', on_delete=models.CASCADE, related_name='cart',verbose_name='کاربر')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='زمان ایجاد')

    def __str__(self):
        return self.user.first_name

    def totalPrice(self):
        try:
            total = sum(item.get_total_price() for item in self.items.all())
        except Exception as e:
            return 0
        return total

    class Meta:
        verbose_name = 'سبد خرید'
        verbose_name_plural = 'سبدهای خرید'

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items', verbose_name='سبد خرید')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='products_in_cart', verbose_name='غذا')
    price = models.BigIntegerField(default=0,verbose_name='قیمت')
    quantity = models.PositiveIntegerField(default=1,verbose_name='تعداد')
    added_at = models.DateTimeField(auto_now_add=True, verbose_name='زمان اضافه شدن')
    expires_at = models.DateTimeField(null=True, blank=True, verbose_name='زمان انقضا')

    def __str__(self):
        return f"{self.product.title} in Cart {self.cart.id}"


    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(hours=2)  # Example: 2 hours expiry
        super().save(*args, **kwargs)

    def get_total_price(self):
        return self.price * self.quantity

    def delete(self, *args, **kwargs):
        # Add quantity back to product inventory
        self.product.inventory += self.quantity
        self.product.save()
        super().delete(*args, **kwargs)

    class Meta:
        verbose_name = 'کالای سبد خرید'
        verbose_name_plural = 'کالاهای سبد خرید'
