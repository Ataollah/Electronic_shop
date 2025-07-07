from django.contrib.admin.sites import AdminSite
import appuser.apps
import blog
import cart.apps
import newsletter
import order.apps
import product.apps
import blog.apps
import siteInfo.apps
import zarinpal.apps
import newsletter.apps


class CustomAdminSite(AdminSite):
    site_header = 'Sufficient'
    site_title = 'پنل ادمین '
    index_title = 'پنل مدیریتی Sufficient'

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
            "Site": 20,
        }
        model_ordering = {
            'AppUser':1,
            'VerificationUser':2,
            'group':3,
            'Cart':4,
            'Order':5,
            'Category':6,
            'Product':7,
            'Questions':8,
            'Banner':9,
            'AboutProduct':10,
            'AboutAfterBeforeProduct':11,
            'CountDownBanner':12,
            'Brands':13,
            'SpecialList':14,
            'Category':15,
            'Post':16,
            'Tag':17,
            'PostComment':18,
            'PostList':19,
            'Subscriber':20,
            'ZarinPal':21,
            'SiteInfo':22,
            'Menu':23,
            'SocialMedia':24,
            'Links':25,
            'Gallery':26,
            'Testimonial':27,
            'FAQ':28,
            'ContactUS':29,
            'SMSProvider':30,
            'MailProvider':31,
            'Province':32,
            'County':33,
            'District':34,
            'City':35,
            'Rural':36,
            'django.contrib.sites':40,
        }
        app_list.sort(key=lambda x: app_ordering.get(x['name'], 100))
        for app in app_list:
            app['models'].sort(key=lambda x: model_ordering.get(x['object_name'], 100))
        return app_list


custom_admin_site = CustomAdminSite(name='custom_admin')
