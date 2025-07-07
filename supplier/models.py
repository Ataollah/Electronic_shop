from django.db import models

# Create your models here.


class Supplier(models.Model):
    name = models.CharField(max_length=255, verbose_name='Supplier Name')
    email = models.EmailField(max_length=255, unique=True, verbose_name='Email Address')
    phone1 = models.CharField(max_length=20, blank=True, null=True, verbose_name='Phone Number')
    phone2 = models.CharField(max_length=20, blank=True, null=True, verbose_name='Phone Number')
    website = models.URLField(blank=True, null=True, verbose_name='Website')
    address = models.TextField(blank=True, null=True, verbose_name='Address')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')

    class Meta:
        verbose_name = 'Supplier'
        verbose_name_plural = 'Suppliers'
        ordering = ['name']

    def __str__(self):
        return self.name

class Salesman(models.Model):
    name = models.CharField(max_length=255, verbose_name='Salesman Name')
    email = models.EmailField(max_length=255, unique=True, verbose_name='Email Address')
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='Phone Number')
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='salesmen', verbose_name='Supplier')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')

    class Meta:
        verbose_name = 'Salesman'
        verbose_name_plural = 'Salesmen'
        ordering = ['name']

    def __str__(self):
        return self.name

class SocialMedia(models.Model):
    salesman = models.ForeignKey(Salesman, on_delete=models.CASCADE, related_name='social_media', verbose_name='Salesman')
    platform = models.CharField(max_length=255, verbose_name='Platform')
    url = models.URLField(verbose_name='Profile URL')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')

    class Meta:
        verbose_name = 'Social Media'
        verbose_name_plural = 'Social Media'
        ordering = ['platform']

    def __str__(self):
        return f"{self.platform} - {self.salesman.name}"
