# apps/energy_fuel_prices/models.py

from django.db import models
from django_jalali.db import models as jmodels
from apps.categories.models import Category


# توجه: EnergyFuelType و Region هم در همین فایل تعریف می‌شوند یا در فایل‌های جداگانه.


class EnergyFuelType(models.Model):
    """
    انواع سوخت و انرژی (برق، گاز، بنزین، گازویل، ...)
    """
    name = models.CharField(verbose_name='نام', max_length=100)
    description = models.TextField(verbose_name='توضیحات', blank=True, null=True)

    class Meta:
        verbose_name = 'نوع سوخت'
        verbose_name_plural = 'انواع سوخت'

    def __str__(self):
        return self.name


class Region(models.Model):
    """
    مناطق جغرافیایی یا استان‌ها جهت محاسبه متفاوت قیمت‌ها.
    """
    name = models.CharField(verbose_name='نام', max_length=100)
    description = models.TextField(verbose_name='توضیحات', blank=True, null=True)

    class Meta:
        verbose_name = 'منطقه'
        verbose_name_plural = 'مناطق'

    def __str__(self):
        return self.name


class PriceSetting(models.Model):
    """
    تنظیمات قیمت‌های پیش‌فرض بر اساس نوع انرژی، فصل، منطقه و نوع کسب‌وکار.
    """
    SEASON_CHOICES = (
        ('spring', 'بهار'),
        ('summer', 'تابستان'),
        ('autumn', 'پاییز'),
        ('winter', 'زمستان'),
    )

    energy_fuel_type = models.ForeignKey(
        EnergyFuelType,
        on_delete=models.CASCADE,
        related_name='price_settings',
        verbose_name='نوع سوخت و انرژی'
    )
    season = models.CharField(
        max_length=50,
        choices=SEASON_CHOICES,
        verbose_name='فصل'
    )
    region = models.ForeignKey(
        Region,
        on_delete=models.SET_NULL,
        null=True,
        related_name='price_settings',
        verbose_name='منطقه'
    )
    business_type = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='price_settings',
        verbose_name='نوع کسب‌وکار'
    )
    base_price = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        verbose_name='قیمت پایه'
    )
    created_at = jmodels.jDateTimeField(
        auto_now_add=True,
        verbose_name='تاریخ ایجاد'
    )
    updated_at = jmodels.jDateTimeField(
        auto_now=True,
        verbose_name='تاریخ به‌روزرسانی'
    )

    class Meta:
        unique_together = ('energy_fuel_type', 'season', 'region', 'business_type')
        verbose_name = 'تنظیم قیمت'
        verbose_name_plural = 'تنظیمات قیمت'

    def __str__(self):
        rgn = self.region.name if self.region else "ناشناخته"
        btype = self.business_type.name if self.business_type else "نامشخص"
        return f"{self.energy_fuel_type.name} - {self.season} - {rgn} - {btype}"
