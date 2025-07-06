from django.db import models

# Create your models here.


class ZarinPal(models.Model):
    merchant_id = models.CharField(max_length=100,verbose_name='Merchant ID')
    request_url = models.URLField(verbose_name='آدرس درخواست')
    verify_url = models.URLField(verbose_name='آدرس تایید')
    start_pay_url = models.URLField(verbose_name='آدرس شروع پرداخت')
    callback_url = models.URLField(verbose_name='آدرس بازگشت')
    sandbox = models.BooleanField(default=True,verbose_name='آزمایشگاهی')
    min_amount = models.IntegerField(default=100000, verbose_name='حداقل مبلغ پرداخت')

    def __str__(self):
        return self.merchant_id

    class Meta:
        verbose_name = 'زرین پال'
        verbose_name_plural = 'زرین پال'