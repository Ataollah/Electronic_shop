from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from Utility.orphan_file_cleaner import update_file_field, delete_file_field
from eshop import settings


class Menu(models.Model):
    name = models.CharField(max_length=200, verbose_name=' نام ')
    url = models.CharField(blank=True, null=True, verbose_name='لینک')
    order = models.IntegerField(default=1, verbose_name='ترتیب')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'منو'
        verbose_name_plural = 'منوها'


class SubMenu(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='submenus', verbose_name='منو')
    name = models.CharField(max_length=200, verbose_name=' نام ')
    url = models.CharField(blank=True, null=True, verbose_name='لینک')
    order = models.IntegerField(default=1, verbose_name='ترتیب')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'زیر منو'
        verbose_name_plural = 'زیر منوها'

class SiteInfo(models.Model):
    name = models.CharField(max_length=200, verbose_name='نام وبسایت')
    slogan = models.CharField(max_length=200,null=True,blank=True, verbose_name='شعار')
    logo_header = models.ImageField(upload_to='website',null=True,blank=True, verbose_name='لوگوسربرگ')
    logo_footer = models.ImageField(upload_to='website',null=True,blank=True, verbose_name='لوگو فوتر')
    email1 = models.EmailField(verbose_name='ایمیل')
    email2 = models.EmailField(null=True,blank=True,verbose_name='ایمیل')
    address = models.CharField(max_length=200, verbose_name='آدرس ')
    telephone1 = models.CharField(max_length=20, verbose_name=' تلفن ')
    telephone2 = models.CharField(null=True,blank=True,max_length=20, verbose_name=' تلفن ')
    copyright = models.CharField(max_length=200, verbose_name=' کپی رایت ')
    copyright_link = models.URLField(default='https://wedosoft.ir', verbose_name='لینک کپی رایت')
    map_url = models.URLField(verbose_name='آدرس گوگل مپ')
    enamad_id = models.CharField(null=True,blank=True,max_length=200, verbose_name='شماره نماد')
    enamad_tag = models.TextField(null=True,blank=True,verbose_name='تگ نماد')
    working_hours = models.TextField(null=True,blank=True,verbose_name='ساعات کاری')
    instagram_id = models.CharField(null=True,blank=True,max_length=200, verbose_name='آیدی اینستاگرام')
    is_selling = models.BooleanField(default=True, verbose_name='فروش فعال')

    def __str__(self):
        return self.name

    def save(self, *arg, **kwargs):
        update_file_field(SiteInfo, self.pk, 'logo_header', self.logo_header)
        update_file_field(SiteInfo, self.pk, 'logo_footer', self.logo_footer)
        super(SiteInfo, self).save(*arg, **kwargs)

    def delete(self, using=None, keep_parents=True):
        delete_file_field(self.logo_header)
        delete_file_field(self.logo_footer)
        super(SiteInfo, self).delete(using, keep_parents)

    class Meta:
        verbose_name = 'اطلاعات وبسایت'
        verbose_name_plural = 'اطلاعات وبسایت'

class SMSProvider(models.Model):
    name = models.CharField(max_length=200, verbose_name='نام ارائه دهنده پیامک')
    api_url = models.URLField(default=None, blank=True, null=True, verbose_name='آدرس ای پی آی ارسال پیامک')
    username = models.CharField(default=None, blank=True, null=True, max_length=100,
                                    verbose_name='نام کاربری پیامک')
    password = models.CharField(default=None, blank=True, null=True, max_length=100, verbose_name='رمز عبور پیامک')
    phone_number = models.CharField(default=None, null=True, blank=True, max_length=100,
                                        verbose_name='شماره ارسال کننده پیامک')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'ارائه دهنده پیامک'
        verbose_name_plural = 'ارائه دهندگان پیامک'

class MailProvider(models.Model):
    name = models.CharField(max_length=200, verbose_name='نام ارائه دهنده ایمیل')
    smtp_sender_email = models.EmailField(default=None, null=True, blank=True, verbose_name='ایمیل فرستنده ایمیل  ')
    smtp_sender_password = models.CharField(default=None, null=True, blank=True, max_length=100,
                                            verbose_name='رمز عبور ایمیل')
    smtp_server = models.CharField(default=None, blank=True, null=True, max_length=100, verbose_name='سرور ایمیل')
    smtp_port = models.IntegerField(default=None, blank=True, null=True, verbose_name='پورت ایمیل')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'ارائه دهنده ایمیل'
        verbose_name_plural = 'ارائه دهندگان ایمیل'

class SocialMedia(models.Model):
    SOCIAL_MEDIA_CHOICES = [
        ('telegram', 'تلگرام'),
        ('instagram', 'اینستاگرام'),
        ('facebook', 'فیسبوک'),
        ('youtube', 'یوتیوب'),
        ('whatsapp', 'واتس اپ'),
        ('linkedin', 'لینکدین'),
        ('pinterest', 'پینترست'),
        ('X', 'ایکس'),
    ]
    url = models.URLField(verbose_name='آدرس')
    type = models.CharField(max_length=20, choices=SOCIAL_MEDIA_CHOICES, default='telegram', verbose_name='نوع')


    class Meta:
        verbose_name = 'شبکه اجتماعی کاربران'
        verbose_name_plural = 'شبکه های اجتماعی کاربران'

    def __str__(self):
        social_dict = dict(self.SOCIAL_MEDIA_CHOICES)
        return social_dict.get(self.type)


class Links(models.Model):
    LINK_TYPE = [('internal', 'داخلی'), ('external', 'خارجی')]
    title = models.CharField(max_length=200, verbose_name='نام')
    url = models.URLField(verbose_name='لینک')
    type = models.CharField(max_length=20, choices=LINK_TYPE, default='Internal', verbose_name='نوع')

    def __str__(self):
        return self.title

    def getTypePersian(self):
        type_dict = dict(self.LINK_TYPE)
        return type_dict.get(self.type)
    getTypePersian.short_description = 'نوع'

    class Meta:
        verbose_name = 'لینک'
        verbose_name_plural = 'لینک ها'

class ContactUS(models.Model):
    name = models.CharField(max_length=200, verbose_name='نام')
    email = models.EmailField(verbose_name='ایمیل')
    phone = models.CharField(max_length=20, null=True,blank=True,verbose_name='تلفن')
    subject = models.CharField(max_length=200, verbose_name='موضوع')
    message = models.TextField(verbose_name='پیام')
    timestamp = models.DateTimeField(auto_now=True,max_length=100, verbose_name='زمان ارسال شمسی')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'تماس با ما'
        verbose_name_plural = 'تماس های با ما'

class FAQ(models.Model):
    question = models.CharField(max_length=200, verbose_name='سوال')
    answer = RichTextUploadingField(verbose_name='پاسخ')
    order = models.IntegerField(default=1, verbose_name='ترتیب')

    def __str__(self):
        return self.question

    class Meta:
        verbose_name = 'سوال و جواب'
        verbose_name_plural = 'سوالات و جواب ها'


class Gallery(models.Model):
    title = models.CharField(max_length=200, verbose_name='عنوان')
    image = models.ImageField(verbose_name="عکس", upload_to="images/", null=True, blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        update_file_field(Gallery, self.id, 'image', self.image)
        super().save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False):
        delete_file_field(self.image)
        super().delete(using,keep_parents)

    class Meta:
        verbose_name = "گالری "
        verbose_name_plural = "گالری "

class Testimonial(models.Model):
    name = models.CharField(max_length=200, verbose_name='نام')
    message = RichTextUploadingField(verbose_name='پیام')
    order = models.IntegerField(default=1, verbose_name='ترتیب')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "تجربه مشتری"
        verbose_name_plural = "تجربیات مشتریان"


