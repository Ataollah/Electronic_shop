from django.contrib import admin
from product.models import *
from jalali_date.admin import ModelAdminJalaliMixin
from eshop.custom_admin import custom_admin_site


# Register your models here.

class InlineGallery(admin.TabularInline):
    model = Gallery
    extra = 1

class QuestionAmin(admin.ModelAdmin):
    model = Questions
    list_display = ('question',)
    list_filter = ('product',)
    search_fields = ('question','answer')


class ProductAdmin(ModelAdminJalaliMixin,admin.ModelAdmin):
    model = Product
    prepopulated_fields = {"slug": ("title",)}
    list_display = ('title', 'current_price', 'category', )
    list_filter = ('category', )
    search_fields = ('title', )
    ordering = ('title',)
    inlines = [InlineGallery,]

class CategoryAdmin(admin.ModelAdmin):
    model = Category
    prepopulated_fields = {"slug": ("title",)}
    list_display = ('title', )
    list_filter = ('title',)
    search_fields = ('title',)
    ordering = ('title',)



    def get_user_fullname(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"
    get_user_fullname.short_description = 'نام کاربر'

    def getShortComment(self, obj):
        return obj.comment[:50]
    getShortComment.short_description = 'نظر'

    def get_food_title(self, obj):
        return obj.food.title

    get_food_title.short_description = 'عنوان '


# class OffersAdmin(ModelAdminJalaliMixin,admin.ModelAdmin):
#     model = Offers
#     list_display = ( 'start_date', 'end_date')
#     search_fields = ('title',)
#     ordering = ('start_date',)

class BannerAdmin(admin.ModelAdmin):
    model = Banner
    list_display = ('small_title','big_title' )
    search_fields = ('small_title','big_title')
    ordering = ('-id',)


class AboutProductAdmin(admin.ModelAdmin):
    model = AboutProduct
    list_display = ('title', )
    search_fields = ('title',)
    ordering = ('-id',)


class AboutAfterBeforeProductAdmin(admin.ModelAdmin):
    model = AboutAfterBeforeProduct
    list_display = ('title', )
    search_fields = ('title',)
    ordering = ('-id',)

class CountDownBannerAdmin(ModelAdminJalaliMixin,admin.ModelAdmin):
    model = CountDownBanner
    list_display = ('title', 'end_date')
    search_fields = ('title',)
    ordering = ('-id',)


class BrandsAdmin(admin.ModelAdmin):
    model = Brands
    list_display = ('title', )
    search_fields = ('title',)
    ordering = ('-id',)


class SpecialListItemInline(admin.TabularInline):
    model = SpecialListItem
    extra = 1
    fields = ('product', 'order')
    ordering = ('order',)
    autocomplete_fields = ('product',)


class SpecialListAdmin(admin.ModelAdmin):
    model = SpecialList
    list_display = ('title', 'order')
    search_fields = ('title',)
    ordering = ('-id',)
    inlines = [SpecialListItemInline,]






custom_admin_site.register(Product,ProductAdmin)
custom_admin_site.register(Questions,QuestionAmin)
custom_admin_site.register(Category,CategoryAdmin)
# custom_admin_site.register(Offers,OffersAdmin)
custom_admin_site.register(Banner,BannerAdmin)
custom_admin_site.register(AboutProduct,AboutProductAdmin)
custom_admin_site.register(AboutAfterBeforeProduct,AboutAfterBeforeProductAdmin)
custom_admin_site.register(CountDownBanner,CountDownBannerAdmin)
custom_admin_site.register(Brands,BrandsAdmin)
custom_admin_site.register(SpecialList,SpecialListAdmin)



