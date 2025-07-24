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


class ProductSpecificationValueInline(admin.TabularInline):
    model = ProductSpecificationValue
    extra = 1
    fields = ('specification', 'value')
    autocomplete_fields = ('specification',)


class ProductAltAdmin(admin.ModelAdmin):
    model = ProductProxy
    list_display = ('title', 'category',)
    list_filter = ('category',)
    search_fields = ('title',)
    ordering = ('title',)
    inlines = [ProductSpecificationValueInline,]

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
    prepopulated_fields = {"slug": ("title",)}
    list_display = ('title', 'order')
    search_fields = ('title',)
    ordering = ('-id',)
    inlines = [SpecialListItemInline,]

class PriceInquiryRequestAdmin(admin.ModelAdmin):
    model = PriceInquiryRequest
    list_display = ('product', 'user', 'created_at')
    search_fields = ('product__title', 'user__email')
    ordering = ('-created_at',)
    list_filter = ('created_at',)

class SpecificationAdmin(admin.ModelAdmin):
    model = Specification
    list_display = ('category__title', 'name')
    search_fields = ('category__title', 'name')
    ordering = ('-id',)
    list_filter = ('category',)


class ProductSpecificationValueAdmin(admin.ModelAdmin):
    model = ProductSpecificationValue
    list_display = ('product', 'specification', 'value')
    search_fields = ('product__title', 'specification__name', 'value')
    ordering = ('-id',)
    list_filter = ('product', 'specification')

class ProductVisitAdmin(admin.ModelAdmin):
    model = ProductVisit
    list_display = ('user', 'product', 'getVisited_PersainDate', 'ip_address', 'device_info')
    search_fields = ('user__username', 'product__title')
    ordering = ('-visited_at',)
    list_filter = ('visited_at',)






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
custom_admin_site.register(PriceInquiryRequest,PriceInquiryRequestAdmin)
custom_admin_site.register(Specification,SpecificationAdmin)
custom_admin_site.register(ProductSpecificationValue,ProductSpecificationValueAdmin)
custom_admin_site.register(ProductVisit,ProductVisitAdmin)
custom_admin_site.register(ProductProxy,ProductAdmin)



