from django.db import models

# Create your models here.


class Supplier(models.Model):
    name = models.CharField(max_length=255, verbose_name='نام تامین کننده')
    email = models.EmailField(max_length=255, blank=True, null=True, verbose_name='ایمیل')
    phone1 = models.CharField(max_length=20, blank=True, null=True, verbose_name='شماره تلفن ۱')
    phone2 = models.CharField(max_length=20, blank=True, null=True, verbose_name='شماره تلفن ۲')
    website = models.URLField(blank=True, null=True, verbose_name='وب سایت')
    address = models.TextField(blank=True, null=True, verbose_name='آدرس')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')


    class Meta:
        verbose_name = 'تامین کننده'
        verbose_name_plural = 'تامین کننده ها'
        ordering = ['name']

    def __str__(self):
        return self.name

class Salesman(models.Model):
    name = models.CharField(max_length=255, verbose_name='نام فروشنده')
    email = models.EmailField(max_length=255, blank=True, null=True, verbose_name='ایمیل فروشنده')
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='شماره موبایل')
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='salesmen', verbose_name='تامین کننده')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')


    class Meta:
        verbose_name = 'فروشنده'
        verbose_name_plural = 'فروشنده ها'
        ordering = ['name']

    def __str__(self):
        return self.name

class SocialMedia(models.Model):
    PLATFORMS = [
        ('telegram', 'تلگرام'),
        ('instagram', 'اینستاگرام'),
        ('facebook', 'فیسبوک'),
        ('youtube', 'یوتیوب'),
        ('whatsapp', 'واتس اپ'),
        ('linkedin', 'لینکدین'),
        ('pinterest', 'پینترست'),
        ('X', 'ایکس'),
    ]
    salesman = models.ForeignKey(Salesman, on_delete=models.CASCADE, related_name='social_media', verbose_name='Salesman')
    platform = models.CharField(max_length=255,choices=PLATFORMS, verbose_name='پلتفرم')
    url = models.URLField(verbose_name='آدرس url')


    class Meta:
        verbose_name = 'شبکه اجتماعی'
        verbose_name_plural = 'شبکه های اجتماعی'
        ordering = ['platform']

    def __str__(self):
        return f"{self.platform} - {self.salesman.name}"
