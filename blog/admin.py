from django.contrib import admin
from django.contrib.admin import ModelAdmin
from jalali_date.admin import ModelAdminJalaliMixin
from blog.models import Post, Category, Tag, PostMedia, PostComment, PostList
from eshop.custom_admin import custom_admin_site


class MediaInline(admin.TabularInline):
    model = PostMedia
    extra = 1  # Number of extra forms to display
    fields = ['type', 'url', 'file']


def get_readonly_fields(self, request, obj=None):
    if obj and obj.type == 'videolink':
        return []
    return ['url']


class PostAdmin(ModelAdminJalaliMixin,ModelAdmin):
    model = Post
    list_display = ('title', 'is_published', 'page_type')
    list_filter = ('page_type','is_published', 'tags')
    search_fields = ('title', 'content','summary','page_type')
    prepopulated_fields = {"slug": ("title",)}
    autocomplete_fields = ['tags','category']
    inlines = [MediaInline]


class PostCategoryAdmin(admin.ModelAdmin):
    model = Category
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ('name',)
    list_display = ('name', )



class TagAdmin(admin.ModelAdmin):
    model = Tag
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ('name',)
    list_display = ('name', )


class PostCommentAdmin(ModelAdminJalaliMixin,admin.ModelAdmin):
    model = PostComment
    list_display = ('get_user_fullname', 'get_post_title','getShortComment','is_published')
    search_fields = ('user__first_name', 'user__last_name', 'post__title','comment')
    fields = ('user', 'post', 'comment', 'is_published','publishedAt','viewed_at')
    list_filter = ('viewed_at',)

    def get_user_fullname(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"
    get_user_fullname.short_description = 'نام کاربر'

    def getShortComment(self, obj):
        return obj.comment[:50]
    getShortComment.short_description = 'نظر'

    def get_post_title(self, obj):
        return obj.post.title
    get_post_title.short_description = 'عنوان پست'

class PostListAdmin(admin.ModelAdmin):
    model = PostList
    list_display = ('title','place')
    list_filter = ('place',)
    search_fields = ('title','place','post')
    autocomplete_fields = ['posts']

custom_admin_site.register(Post,PostAdmin)
custom_admin_site.register(PostComment,PostCommentAdmin)
custom_admin_site.register(Tag,TagAdmin)
custom_admin_site.register(Category,PostCategoryAdmin)
custom_admin_site.register(PostList,PostListAdmin)