from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from ckeditor.fields import RichTextField
from django.urls import reverse
from django.utils.text import slugify
from Utility.orphan_file_cleaner import update_file_field, delete_file_field
from appuser.models import  AppUser

class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name=' عنوان نوع ')
    slug = models.SlugField(max_length=200, unique=True, verbose_name='اسلاگ ', allow_unicode=True)

    class Meta:
        verbose_name = 'نوع پست'
        verbose_name_plural = 'انواع پست'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super(Category, self).save(*args, **kwargs)

class Post(models.Model):
    MEDIA_TYPE_CHOICES = [
        ('no_picture', 'بدون تصویر'),
        ('audio', 'صدا'),
        ('one_picture', 'عکس'),
        ('multi_picture', 'چند عکس'),
        ('local_video', 'فیلم'),
        ('video_link', 'لینک به ویدیو سایر پلت فرم ها'),

    ]
    PAGE_TYPE_CHOICES = [
        ('about_us', 'درباره ما'),
        ('contact_us', 'تماس باما'),
        ('privacy_policy', 'حریم خصوصی'),
        ('terms_of_use', 'مقررات'),
        ('banner','بنر صفحه اصلی'),
        ('normal', 'صفحه معمولی')
    ]
    page_type = models.CharField(max_length=20, choices=PAGE_TYPE_CHOICES, default='normal',
                                 verbose_name='نوع صفحه')
    title = models.CharField(max_length=200, error_messages={'required': 'پرکن'}, verbose_name='عنوان فارسی')
    sub_title = models.CharField(max_length=200, verbose_name='عنوان فارسی فرعی', blank=True, null=True)
    keyword = models.CharField(max_length=200, verbose_name='کلمات کلیدی', blank=True, null=True)
    slug = models.SlugField(max_length=200, unique=True, verbose_name='اسلاگ فارسی', allow_unicode=True)
    summary = RichTextField(verbose_name=' خلاصه فارسی')
    is_published = models.BooleanField(default=False, verbose_name='منتشر شده؟')
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ انتشار ')
    updatedAt = models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')
    publishedAt = models.DateTimeField(blank=True, null=True, verbose_name='تاریخ انتشار')
    content = RichTextUploadingField(verbose_name='متن فارسی')
    author = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='posts', verbose_name='نویسنده')
    category = models.ForeignKey(Category,null=True,blank=True, on_delete=models.CASCADE, related_name='category', verbose_name='نوع پست')
    tags = models.ManyToManyField('Tag', verbose_name='برچسب ها', blank=True)
    post_media_type = models.CharField(max_length=20, choices=MEDIA_TYPE_CHOICES, default='no_picture',
                                       verbose_name='نوع رسانه')

    def get_absolute_url(self):
        return reverse('blog-detail-view', args=[str(self.slug)])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        super(Post, self).save(*args, **kwargs)

    PAGE_TYPE_DICT = dict(PAGE_TYPE_CHOICES)
    def __str__(self):
        return f"{self.title}{'----- نوع : '}{ self.PAGE_TYPE_DICT.get(self.page_type)} "

    class Meta:
        verbose_name = 'پست'
        verbose_name_plural = 'پست ها'

class PostList(models.Model):
    PLACE_TYPE_CHOICES = [
        ('main_page', 'صفحه اصلی'),
        ('blog_page', 'صفحه بلاگ'),
        ('footer','فوتر'),
    ]
    title = models.CharField(max_length=200, verbose_name='عنوان')
    place = models.CharField(choices=PLACE_TYPE_CHOICES,default='blog_page',max_length=200, verbose_name='مکان')
    posts = models.ManyToManyField(Post, related_name='post_lists', verbose_name='پست ها')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'لیست پست'
        verbose_name_plural = 'لیست پست ها'

class Like(models.Model):
    session_key = models.CharField(max_length=40)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('session_key', 'post')

class PostMedia(models.Model):
    MEDIA_TYPE_CHOICES = [
        ('image', 'عکس'),
        ('audio', 'صدا'),
        ('poster','عکس جایگزین فیلم'),
        ('localvideo', 'فیلم'),
        ('videolink', 'لینک به ویدیو سایر پلت فرم ها'),
    ]
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='media', verbose_name='پست')
    url = models.URLField(verbose_name='آدرس', blank=True, null=True)
    file = models.FileField(upload_to='media/', verbose_name='فایل', blank=True, null=True)
    type = models.CharField(max_length=20, choices=MEDIA_TYPE_CHOICES, default='image')

    def save(self, *args, **kwargs):
        update_file_field(PostMedia, self.pk, 'file', self.file)
        super(PostMedia, self).save(*args, **kwargs)

    def delete(self, using=None, keep_parents=True):
        delete_file_field(self.file)
        super(PostMedia, self).delete()

    class Meta:
        verbose_name = 'رسانه'
        verbose_name_plural = 'رسانه ها'

    def __str__(self):
        return self.post.title

class PostComment(models.Model):
    post = models.ForeignKey(Post,related_name='post_comments', on_delete=models.CASCADE, verbose_name='پست')
    comment = models.TextField(verbose_name='نظر')
    publishedAt = models.DateTimeField(null=True,blank=True, verbose_name='تاریخ انتشار')
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    viewed_at = models.DateTimeField(null=True,blank=True, verbose_name='تاریخ مشاهده')
    is_published = models.BooleanField(default=False, verbose_name='منتشر شده ؟')
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='comments')

    class Meta:
        verbose_name = 'نظرهای پست'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.comment

class Tag(models.Model):
    name = models.CharField(max_length=200, verbose_name=' عنوان برچسب ')
    slug = models.SlugField(max_length=200, unique=True, verbose_name='اسلاگ ', allow_unicode=True)

    class Meta:
        verbose_name = 'برچسب'
        verbose_name_plural = 'برچسب ها'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super(Tag, self).save(*args, **kwargs)
