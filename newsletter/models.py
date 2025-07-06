from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models

# Create your models here.


class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'مشترک خبرنامه'
        verbose_name_plural = 'مشترکین خبرنامه'

class Newsletter(models.Model):
    subject = models.CharField(max_length=255,verbose_name='موضوع')
    body = RichTextUploadingField(verbose_name='متن')
    created_at = models.DateTimeField(auto_now_add=True,verbose_name='تاریخ ایجاد')
    send_at = models.DateTimeField(null=True,blank=True,verbose_name='تاریخ ارسال')

    def __str__(self):
        return self.subject[:50]


    class Meta:
        verbose_name = 'خبرنامه'
        verbose_name_plural = 'خبرنامه ها'