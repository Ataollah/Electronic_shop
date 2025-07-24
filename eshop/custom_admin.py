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
            'ProductProxy': 10,
            'ProductVisit': 11,
            'ProductSpecificationValue': 12,
            'Questions': 13,
            'Banner': 14,
            'AboutProduct': 15,
            'AboutAfterBeforeProduct': 16,
            'CountDownBanner': 17,
            'Brands': 18,
            'SpecialList': 19,
            'Post': 20,
            'Tag': 21,
            'PostComment': 22,
            'PostList': 23,
            'Subscriber': 24,
            'ZarinPal': 25,
            'SiteInfo': 26,
            'Menu': 27,
            'SocialMedia': 28,
            'Links': 29,
            'Gallery': 30,
            'Testimonial': 31,
            'FAQ': 32,
            'ContactUS': 33,
            'SMSProvider': 34,
            'MailProvider': 35,
            'Province': 36,
            'County': 37,
            'District': 38,
            'City': 39,
            'Rural': 40,
            'Supplier': 41,
            'Salesman': 42,
            'django.contrib.sites': 43,
        }
        app_list.sort(key=lambda x: app_ordering.get(x['name'], 100))
        for app in app_list:
            app['models'].sort(key=lambda x: model_ordering.get(x['object_name'], 100))
        return app_list


custom_admin_site = CustomAdminSite(name='custom_admin')
