from django.apps import AppConfig


class SiteInfoConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "siteInfo"
    verbose_name = "مدیریت اطلاعات سایت"

    def ready(self):
        # Import signals to ensure they are registered
        from siteInfo import signals