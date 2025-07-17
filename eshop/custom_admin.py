from django.contrib.admin.sites import AdminSite
import appuser.apps
import blog
import cart.apps
import newsletter
import order.apps
import product.apps
import blog.apps
import siteInfo.apps
import supplier
import zarinpal.apps
import newsletter.apps
import supplier.apps
import iran.apps


class CustomAdminSite(AdminSite):
    site_header = 'E-Shop'
    site_title = 'پنل ادمین '
    index_title = 'پنل مدیریتی E-Shop'

    def get_app_list(self, request, *args, **kwargs):
        app_list = super().get_app_list(request)
        app_ordering = {
            appuser.apps.AppuserConfig.verbose_name: 1,
            'بررسی اصالت و اجازه‌ها': 2,
            cart.apps.CartConfig.verbose_name: 3,
            order.apps.OrderConfig.verbose_name: 4,
            product.apps.ProductConfig.verbose_name: 5,
            blog.apps.BlogConfig.verbose_name: 6,
            newsletter.apps.NewsletterConfig.verbose_name: 7,
            zarinpal.apps.ZarinpalConfig.verbose_name: 9,
            siteInfo.apps.SiteInfoConfig.verbose_name: 10,
            iran.apps.IranConfig.verbose_name: 11,
            supplier.apps.SupplierConfig.verbose_name: 12,
            "Site": 20,
        }
        model_ordering = {
            'AppUser': 1,
            'PageVisit': 2,
            'VerificationUser': 3,
            'group': 4,
            'Cart': 5,
            'Order': 6,
            'Category': 7,
            'Specification': 8,
            'Product': 9,
            'ProductVisit': 10,
            'ProductSpecificationValue': 11,
            'Questions': 12,
            'Banner': 13,
            'AboutProduct': 14,
            'AboutAfterBeforeProduct': 15,
            'CountDownBanner': 16,
            'Brands': 17,
            'SpecialList': 18,
            'Post': 19,
            'Tag': 20,
            'PostComment': 21,
            'PostList': 22,
            'Subscriber': 23,
            'ZarinPal': 24,
            'SiteInfo': 25,
            'Menu': 26,
            'SocialMedia': 27,
            'Links': 28,
            'Gallery': 29,
            'Testimonial': 30,
            'FAQ': 31,
            'ContactUS': 32,
            'SMSProvider': 33,
            'MailProvider': 34,
            'Province': 35,
            'County': 36,
            'District': 37,
            'City': 38,
            'Rural': 39,
            'Supplier': 40,
            'Salesman': 41,
            'django.contrib.sites': 42,
        }
        app_list.sort(key=lambda x: app_ordering.get(x['name'], 100))
        for app in app_list:
            app['models'].sort(key=lambda x: model_ordering.get(x['object_name'], 100))
        return app_list


custom_admin_site = CustomAdminSite(name='custom_admin')
