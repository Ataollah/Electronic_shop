from django.apps import AppConfig


class SiteInfoConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "siteInfo"
    verbose_name = "مدیریت اطلاعات سایت"

    def ready(self):
        import siteInfo.signals
        # Import the signals module to ensure the signal handlers are registered
        # when the app is ready.
