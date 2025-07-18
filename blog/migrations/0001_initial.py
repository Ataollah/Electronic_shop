# Generated by Django 5.2.1 on 2025-07-06 17:21

import ckeditor.fields
import ckeditor_uploader.fields
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=200, verbose_name=" عنوان نوع ")),
                (
                    "slug",
                    models.SlugField(
                        allow_unicode=True,
                        max_length=200,
                        unique=True,
                        verbose_name="اسلاگ ",
                    ),
                ),
            ],
            options={
                "verbose_name": "نوع پست",
                "verbose_name_plural": "انواع پست",
            },
        ),
        migrations.CreateModel(
            name="Tag",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(max_length=200, verbose_name=" عنوان برچسب "),
                ),
                (
                    "slug",
                    models.SlugField(
                        allow_unicode=True,
                        max_length=200,
                        unique=True,
                        verbose_name="اسلاگ ",
                    ),
                ),
            ],
            options={
                "verbose_name": "برچسب",
                "verbose_name_plural": "برچسب ها",
            },
        ),
        migrations.CreateModel(
            name="Post",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "page_type",
                    models.CharField(
                        choices=[
                            ("about_us", "درباره ما"),
                            ("contact_us", "تماس باما"),
                            ("privacy_policy", "حریم خصوصی"),
                            ("terms_of_use", "مقررات"),
                            ("banner", "بنر صفحه اصلی"),
                            ("normal", "صفحه معمولی"),
                        ],
                        default="normal",
                        max_length=20,
                        verbose_name="نوع صفحه",
                    ),
                ),
                (
                    "title",
                    models.CharField(
                        error_messages={"required": "پرکن"},
                        max_length=200,
                        verbose_name="عنوان فارسی",
                    ),
                ),
                (
                    "sub_title",
                    models.CharField(
                        blank=True,
                        max_length=200,
                        null=True,
                        verbose_name="عنوان فارسی فرعی",
                    ),
                ),
                (
                    "keyword",
                    models.CharField(
                        blank=True,
                        max_length=200,
                        null=True,
                        verbose_name="کلمات کلیدی",
                    ),
                ),
                (
                    "slug",
                    models.SlugField(
                        allow_unicode=True,
                        max_length=200,
                        unique=True,
                        verbose_name="اسلاگ فارسی",
                    ),
                ),
                ("summary", ckeditor.fields.RichTextField(verbose_name=" خلاصه فارسی")),
                (
                    "is_published",
                    models.BooleanField(default=False, verbose_name="منتشر شده؟"),
                ),
                (
                    "createdAt",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="تاریخ انتشار "
                    ),
                ),
                (
                    "updatedAt",
                    models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی"),
                ),
                (
                    "publishedAt",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="تاریخ انتشار"
                    ),
                ),
                (
                    "content",
                    ckeditor_uploader.fields.RichTextUploadingField(
                        verbose_name="متن فارسی"
                    ),
                ),
                (
                    "post_media_type",
                    models.CharField(
                        choices=[
                            ("no_picture", "بدون تصویر"),
                            ("audio", "صدا"),
                            ("one_picture", "عکس"),
                            ("multi_picture", "چند عکس"),
                            ("local_video", "فیلم"),
                            ("video_link", "لینک به ویدیو سایر پلت فرم ها"),
                        ],
                        default="no_picture",
                        max_length=20,
                        verbose_name="نوع رسانه",
                    ),
                ),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="posts",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="نویسنده",
                    ),
                ),
                (
                    "category",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="category",
                        to="blog.category",
                        verbose_name="نوع پست",
                    ),
                ),
                (
                    "tags",
                    models.ManyToManyField(
                        blank=True, to="blog.tag", verbose_name="برچسب ها"
                    ),
                ),
            ],
            options={
                "verbose_name": "پست",
                "verbose_name_plural": "پست ها",
            },
        ),
        migrations.CreateModel(
            name="PostComment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("comment", models.TextField(verbose_name="نظر")),
                (
                    "publishedAt",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="تاریخ انتشار"
                    ),
                ),
                (
                    "createdAt",
                    models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد"),
                ),
                (
                    "viewed_at",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="تاریخ مشاهده"
                    ),
                ),
                (
                    "is_published",
                    models.BooleanField(default=False, verbose_name="منتشر شده ؟"),
                ),
                (
                    "post",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="post_comments",
                        to="blog.post",
                        verbose_name="پست",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="comments",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "نظرهای پست",
                "verbose_name_plural": "نظرهای پست",
            },
        ),
        migrations.CreateModel(
            name="PostList",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=200, verbose_name="عنوان")),
                (
                    "place",
                    models.CharField(
                        choices=[
                            ("main_page", "صفحه اصلی"),
                            ("blog_page", "صفحه بلاگ"),
                            ("footer", "فوتر"),
                        ],
                        default="blog_page",
                        max_length=200,
                        verbose_name="مکان",
                    ),
                ),
                (
                    "posts",
                    models.ManyToManyField(
                        related_name="post_lists", to="blog.post", verbose_name="پست ها"
                    ),
                ),
            ],
            options={
                "verbose_name": "لیست پست",
                "verbose_name_plural": "لیست پست ها",
            },
        ),
        migrations.CreateModel(
            name="PostMedia",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("url", models.URLField(blank=True, null=True, verbose_name="آدرس")),
                (
                    "file",
                    models.FileField(
                        blank=True, null=True, upload_to="media/", verbose_name="فایل"
                    ),
                ),
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("image", "عکس"),
                            ("audio", "صدا"),
                            ("poster", "عکس جایگزین فیلم"),
                            ("localvideo", "فیلم"),
                            ("videolink", "لینک به ویدیو سایر پلت فرم ها"),
                        ],
                        default="image",
                        max_length=20,
                    ),
                ),
                (
                    "post",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="media",
                        to="blog.post",
                        verbose_name="پست",
                    ),
                ),
            ],
            options={
                "verbose_name": "رسانه",
                "verbose_name_plural": "رسانه ها",
            },
        ),
        migrations.CreateModel(
            name="Like",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("session_key", models.CharField(max_length=40)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "post",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="blog.post"
                    ),
                ),
            ],
            options={
                "unique_together": {("session_key", "post")},
            },
        ),
    ]
