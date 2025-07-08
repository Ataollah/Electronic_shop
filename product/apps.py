from django.apps import AppConfig


class ProductConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "product"
    verbose_name = "محصولات"

    def ready(self):
        # Import signals to ensure they are registered
        from product import signals
