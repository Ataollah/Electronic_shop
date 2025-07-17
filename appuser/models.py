from django.contrib.auth.models import AbstractUser
from django.db import models
from Utility.orphan_file_cleaner import update_file_field, delete_file_field
import jdatetime


class VerificationUser(models.Model):
    username = models.CharField(max_length=50, blank=False, unique=False, verbose_name='نام کاربری')
    verification_code = models.CharField(max_length=50, blank=False, verbose_name='کد تایید')
    valid_until = models.DateTimeField(blank=True, verbose_name='اعتبار کد تایید')

    class Meta:
        verbose_name = 'کاربر موقت'
        verbose_name_plural = 'کاربران موقت'

    def __str__(self):
        return self.username

class AppUser(AbstractUser):
    profile_picture = models.ImageField(verbose_name="عکس پروفایل", null=True, blank=True, upload_to="profile_pictures/")
    province = models.CharField(max_length=100,default='تهران', verbose_name='استان')
    county = models.CharField(max_length=100,default='تهران', verbose_name='شهرستان')
    district = models.CharField(max_length=100, default='مرکزی', verbose_name='منطقه')
    city = models.CharField(max_length=100, default='تهران', verbose_name='شهر')
    rural = models.CharField(max_length=100, blank=True,null=True, verbose_name='روستا')
    address = models.TextField(blank=True,null=True,verbose_name='آدرس')
    postal_code = models.CharField(max_length=10, verbose_name='کد پستی', blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    get_full_name.short_description = 'نام کامل'

    def get_full_address(self):
        return f"{self.province} - {self.county} - {self.district} - {self.city} - {self.rural} - {self.address} -  {self.postal_code}"
    get_full_address.short_description = 'آدرس کامل'

    def isCustomer(self):
        if self.groups.filter(name='Customer').exists():
            return True
        return False
    isCustomer.short_description = 'مشتری'
    isCustomer.boolean = True

    def isCashier(self):
        if self.groups.filter(name='Cashier').exists():
            return True
        return False
    isCashier.short_description = 'صندوق دار'
    isCashier.boolean = True

    def isManager(self):
        if self.groups.filter(name='Manager').exists():
            return True
        return False
    isManager.short_description = 'مدیر'
    isManager.boolean = True

    # Python code
    def isSuperUser(self):
        return self.is_superuser

    isSuperUser.short_description = 'سوپر یوزر'
    isSuperUser.boolean = True

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'


class PageVisit(models.Model):
    user = models.ForeignKey(AppUser, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='کاربر')
    ip_address = models.GenericIPAddressField(null=True, blank=True,verbose_name='آدرس آی پی')
    device_info = models.CharField(max_length=255, null=True, blank=True,verbose_name='اطلاعات دستگاه')
    page_url = models.CharField(max_length=255,verbose_name='آدرس صفحه')
    visited_at = models.DateTimeField(auto_now_add=True,verbose_name='زمان بازدید')

    def getVisited_PersainDate(self):
        if self.visited_at:
            jalali_date = jdatetime.datetime.fromgregorian(datetime=self.visited_at)
            return jalali_date.strftime('%Y/%m/%d %H:%M')
        return ''
    getVisited_PersainDate.short_description = 'زمان بازدید (شمسی)'

    def __str__(self):
        return f"{self.user or self.ip_address} visited {self.page_url} at {self.visited_at}"

    class Meta:
        verbose_name = 'بازدید صفحه'
        verbose_name_plural = 'بازدیدهای صفحه'
        ordering = ['-visited_at']








