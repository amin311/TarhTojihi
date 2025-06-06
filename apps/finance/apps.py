from django.apps import AppConfig


class FinanceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.finance'
    verbose_name = 'ماژول مالی'

    def ready(self):
        # ثبت سیگنال‌ها
        from . import signals  # noqa 