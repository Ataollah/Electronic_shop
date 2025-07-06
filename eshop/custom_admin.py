from django.contrib.admin.sites import AdminSite
import appuser.apps
import siteInfo.apps


class CustomAdminSite(AdminSite):
    site_header = 'Sufficient'
    site_title = 'پنل ادمین '
    index_title = 'پنل مدیریتی Sufficient'

    def get_app_list(self, request, *args, **kwargs):
        app_list = super().get_app_list(request)
        app_ordering = {
            appuser.apps.AppuserConfig.verbose_name: 1,
            'بررسی اصالت و اجازه‌ها': 2,
            siteInfo.apps.SiteInfoConfig.verbose_name: 3,
            "Site": 20,
        }
        model_ordering = {
            'appuser':1,
            'VerificationCode':2,
            'group':3,
            'django.contrib.sites':40,
        }
        app_list.sort(key=lambda x: app_ordering.get(x['name'], 100))
        for app in app_list:
            app['models'].sort(key=lambda x: model_ordering.get(x['object_name'], 100))
        return app_list


custom_admin_site = CustomAdminSite(name='custom_admin')
