from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.urls import reverse
from django.conf import settings

from Utility.orphan_file_cleaner import update_file_field, delete_file_field
from django.core.validators import MinValueValidator, MaxValueValidator
import datetime

# Create your models here.

class Category(models.Model):
    title = models.CharField(verbose_name="عنوان", max_length=100)
    image = models.ImageField(verbose_name="عکس",null=True,blank=True, upload_to="images/")
    slug = models.SlugField(verbose_name="اسلاگ", unique=True,allow_unicode=True)
    order = models.IntegerField(verbose_name="ترتیب", default=0)
    show_on_homepage = models.BooleanField(verbose_name="نمایش در صفحه اصلی", default=False)

    def save(self, *args, **kwargs):
        update_file_field(Category, self.id, 'image', self.image)
        super().save(*args, **kwargs)


    def delete(self, using = None, keep_parents = False):
        delete_file_field(self.image)
        super().delete(using, keep_parents)


    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "نوع محصول"
        verbose_name_plural = "انواع محصولات"

class Product(models.Model):
    category = models.ForeignKey(Category, verbose_name="نوع ", on_delete=models.CASCADE,null=True)
    show_on_homepage = models.BooleanField(verbose_name="نمایش در صفحه اصلی", default=False)
    order = models.IntegerField(verbose_name="ترتیب نمایش", default=0)
    title = models.CharField(verbose_name="عنوان", max_length=100)
    slug = models.SlugField(verbose_name="اسلاگ", unique=True,allow_unicode=True)
    current_price = models.BigIntegerField(verbose_name="قیمت فعلی", default=0)
    discount = models.SmallIntegerField(verbose_name="درصد تخفیف", default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    old_price = models.BigIntegerField(verbose_name="قیمت قبلی", default=0)
    inventory = models.IntegerField(verbose_name="موجودی", default=0)
    short_description = RichTextUploadingField(verbose_name='توضیحات کوتاه', null=True, blank=True)
    description = RichTextUploadingField(verbose_name='توضیحات ', null=True, blank=True)
    primary_image = models.ImageField(verbose_name="عکس اصلی", null=True, blank=True, upload_to="images/")
    secondary_image = models.ImageField(verbose_name="عکس اصلی", null=True, blank=True, upload_to="images/")
    image_tag = models.TextField(verbose_name="برچسب عکس", null=True, blank=True)
    offer_start_date = models.DateField(verbose_name="تاریخ شروع", auto_now=True)
    offer_end_date = models.DateTimeField(verbose_name="تاریخ انقضا", null=True, blank=True, default=datetime.datetime.now)
    price_inquiry = models.BooleanField(verbose_name="درخواست قیمت", default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product-detail-view', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        update_file_field(Product, self.id, 'primary_image', self.primary_image)
        update_file_field(Product, self.id, 'secondary_image', self.secondary_image)
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        delete_file_field(self.primary_image)
        delete_file_field(self.secondary_image)
        super().delete(*args, **kwargs)

    class Meta:
        verbose_name = "محصول"
        verbose_name_plural = "محصولات"
        ordering = ['-id']

class Gallery(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', verbose_name="محصول")
    image = models.ImageField(verbose_name="عکس", null=True, blank=True, upload_to="images/")
    thumbnail = models.ImageField(verbose_name="عکس بندانگشتی", null=True, blank=True, upload_to="images/")
    order = models.IntegerField(verbose_name="ترتیب", default=0)

    def save(self, *args, **kwargs):
        update_file_field(Gallery, self.id, 'image', self.image)
        update_file_field(Gallery, self.id, 'thumbnail', self.thumbnail)
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        delete_file_field(self.image)
        delete_file_field(self.thumbnail)
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"گالری محصول: {self.product.title} - عکس {self.order}"

    class Meta:
        verbose_name = "گالری محصول"
        verbose_name_plural = "گالری محصولات"
        ordering = ['order']

class Questions(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='questions', verbose_name="محصول")
    question = models.TextField(verbose_name="سوال")
    answer = models.TextField(verbose_name="جواب")
    order = models.IntegerField(verbose_name="ترتیب", default=0)

    class Meta:
        verbose_name = "سوال و جواب"
        verbose_name_plural = "سوالات و جواب ها"

    def __str__(self):
        return f"محصول: {self.product.title} - شماره سوال {self.order}"


class Banner(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='banners', verbose_name="محصول")
    small_title = models.CharField(default='title',verbose_name="عنوان ریز", max_length=100)
    big_title = models.CharField(default='title',verbose_name="عنوان درشت", max_length=100)
    image = models.ImageField(verbose_name="عکس", null=True, blank=True, upload_to="images/")
    description = models.TextField(verbose_name="توضیحات", null=True, blank=True)
    order = models.IntegerField(verbose_name="ترتیب", default=0)

    def save(self, *args, **kwargs):
        update_file_field(Banner, self.id, 'image', self.image)
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        delete_file_field(self.image)
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.small_title

    class Meta:
        verbose_name = "بنر"
        verbose_name_plural = "بنرها"

class AboutProduct(models.Model):
    DIR = [
        ('RTL', 'سمت راست'),
        ('LTR', 'سمت چپ'),
    ]
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='about', verbose_name="محصول")
    title = models.CharField(verbose_name="عنوان", max_length=100)
    description = RichTextUploadingField(verbose_name='توضیحات', null=True, blank=True)
    image = models.ImageField(verbose_name="عکس", null=True, blank=True, upload_to="images/")
    direction = models.CharField(verbose_name="جای متن در صفحه", max_length=3, choices=DIR, default='RTL')
    order = models.IntegerField(verbose_name="ترتیب", default=0)

    def __str__(self):
        return f" {self.title}"

    def save(self, *args, **kwargs):
        update_file_field(AboutProduct, self.id, 'image', self.image)
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        delete_file_field(self.image)
        super().delete(*args, **kwargs)

    class Meta:
        verbose_name = "درباره محصول"
        verbose_name_plural = "درباره محصولات"

class AboutAfterBeforeProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='about_after_before', verbose_name="محصول")
    title = models.CharField(verbose_name="عنوان", max_length=100)
    description = RichTextUploadingField(verbose_name='توضیحات', null=True, blank=True)
    image_before = models.ImageField(verbose_name="عکس قبل", null=True, blank=True, upload_to="images/")
    image_after = models.ImageField(verbose_name="عکس بعد", null=True, blank=True, upload_to="images/")

    def __str__(self):
        return f"{self.product.title} - {self.title}"

    def save(self, *args, **kwargs):
        update_file_field(AboutProduct, self.id, 'image_before', self.image_before)
        update_file_field(AboutAfterBeforeProduct, self.id, 'image_after', self.image_after)
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        delete_file_field(self.image_before)
        delete_file_field(self.image_after)
        super().delete(*args, **kwargs)

    class Meta:
        verbose_name = "قبل و بعد از محصول"
        verbose_name_plural = "قبل و بعد از محصول"

class CountDownBanner(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='countdown_banners', verbose_name="محصول")
    title = models.CharField(verbose_name="عنوان", max_length=100)
    image_left = models.ImageField(verbose_name="عکس چپ", null=True, blank=True, upload_to="images/")
    image_right = models.ImageField(verbose_name="عکس راست", null=True, blank=True, upload_to="images/")
    description = models.TextField(verbose_name="توضیحات", null=True, blank=True)
    start_date = models.DateField(verbose_name="تاریخ شروع",auto_now=True)
    end_date = models.DateTimeField(verbose_name="تاریخ شمارش معکوس",null=True, blank=True,default=datetime.datetime.now)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        update_file_field(CountDownBanner, self.id, 'image_left', self.image_left)
        update_file_field(CountDownBanner, self.id, 'image_right', self.image_left)
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        delete_file_field(self.image_left)
        delete_file_field(self.image_right)
        super().delete(*args, **kwargs)

    class Meta:
        verbose_name = "بنر شمارش معکوس"
        verbose_name_plural = "بنرهای شمارش معکوس"

class Brands(models.Model):
    title = models.CharField(verbose_name="نام برند", max_length=100)
    image = models.ImageField(verbose_name="عکس", null=True, blank=True, upload_to="images/")
    order = models.IntegerField(verbose_name="ترتیب نمایش", default=0)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        update_file_field(Brands, self.id, 'image', self.image)
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        delete_file_field(self.image)
        super().delete(*args, **kwargs)

    class Meta:
            verbose_name = "برند"
            verbose_name_plural = "برندها"


class SpecialList(models.Model):
    title = models.CharField(verbose_name="عنوان", max_length=100)
    slug = models.SlugField(verbose_name="اسلاگ", unique=True, allow_unicode=True)
    order = models.IntegerField(verbose_name="ترتیب نمایش", default=0)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "لیست ویژه"
        verbose_name_plural = "لیست های ویژه"
        ordering = ['order']

class SpecialListItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='special_list_items', verbose_name="محصول")
    special_list = models.ForeignKey(SpecialList, on_delete=models.CASCADE, related_name='items', verbose_name="لیست ویژه")
    show_on_homepage = models.BooleanField(verbose_name="نمایش در صفحه اصلی", default=False)
    order = models.IntegerField(verbose_name="ترتیب نمایش", default=0)

    def __str__(self):
        return f"{self.product.title} - {self.special_list.title}"

    class Meta:
        verbose_name = "آیتم لیست ویژه"
        verbose_name_plural = "آیتم های لیست ویژه"
        ordering = ['order']


class PriceInquiryRequest(models.Model):
    REQUEST_STATUS = [
        ('waiting', 'در انتظار'),
        ('answered', 'پاسخ داده شده'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='price_inquiries')
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='price_inquiries')
    status = models.CharField(max_length=20, choices=REQUEST_STATUS, default='waiting', verbose_name="وضعیت")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "درخواست استعلام قیمت"
        verbose_name_plural = "درخواست‌های استعلام قیمت"
        ordering = ['-created_at']


    @classmethod
    def get_or_create_waiting(cls, user, product):
        if not user.is_authenticated:
            return None, False
        inquiry = cls.objects.filter(user=user, product=product, status='waiting').first()
        if inquiry:
            return inquiry, False
        return cls.objects.create(user=user, product=product), True

    def __str__(self):
        return f"{self.user} - {self.product} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"
