from django.db import models

# Create your models here.

class Province(models.Model):
    name = models.CharField(max_length=100, verbose_name='نام استان')
    slug = models.SlugField(unique=True, allow_unicode=True, verbose_name='اسلاگ')
    tel_prefix = models.CharField(max_length=20, verbose_name='پیش شماره استان')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'استان'
        verbose_name_plural = 'استان‌ها'


class County(models.Model):
    name = models.CharField(max_length=100, verbose_name='نام شهرستان')
    slug = models.SlugField(unique=True, allow_unicode=True, verbose_name='اسلاگ')
    province = models.ForeignKey(Province, on_delete=models.CASCADE, related_name='counties', verbose_name='استان')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'شهرستان'
        verbose_name_plural = 'شهرستان‌ها'


class City(models.Model):
    name = models.CharField(max_length=100, verbose_name='نام شهر')
    slug = models.SlugField(unique=True, allow_unicode=True, verbose_name='اسلاگ')
    county = models.ForeignKey(County, on_delete=models.CASCADE, related_name='cities', verbose_name='شهرستان')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'شهر'
        verbose_name_plural = 'شهرها'

class District(models.Model):
    name = models.CharField(max_length=100, verbose_name='نام منطقه')
    slug = models.SlugField(unique=True, allow_unicode=True, verbose_name='اسلاگ')
    county = models.ForeignKey(County, on_delete=models.CASCADE, related_name='districts', verbose_name='شهر')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'منطقه'
        verbose_name_plural = 'منطقه‌ها'

class Rural(models.Model):
    name = models.CharField(max_length=100, verbose_name='نام روستا')
    slug = models.SlugField(unique=True, allow_unicode=True, verbose_name='اسلاگ')
    county = models.ForeignKey(County, on_delete=models.CASCADE, related_name='rurals', verbose_name='منطقه')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'روستا'
        verbose_name_plural = 'روستاها'



