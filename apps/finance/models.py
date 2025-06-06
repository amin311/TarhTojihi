from django.db import models
from django_jalali.db import models as jmodels
from apps.projects.models import Project
from apps.categories.models import FinancialTable


class ProjectFinancialData(models.Model):
    """داده‌های هر جدول مالی برای یک پروژه مشخص."""

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='financial_data',
        verbose_name='پروژه'
    )
    financial_table = models.ForeignKey(
        FinancialTable,
        on_delete=models.CASCADE,
        related_name='project_data',
        verbose_name='جدول مالی'
    )
    # داده‌های مربوط به ردیف/ستون‌های جدول به‌صورت JSON ذخیره می‌شود
    # انتظار می‌رود ساختار داده به صورت لیستی از دیکشنری‌ها باشد
    data = models.JSONField(verbose_name='داده جدول')

    # شاخص‌های محاسبه‌ شده مانند جمع ستون‌ها، NPV، IRR و ...
    computed_metrics = models.JSONField(
        verbose_name='شاخص‌های محاسبه‌شده',
        blank=True,
        null=True
    )

    created_at = jmodels.jDateTimeField(auto_now_add=True, verbose_name='ایجاد')
    updated_at = jmodels.jDateTimeField(auto_now=True, verbose_name='به‌روزرسانی')

    class Meta:
        unique_together = ('project', 'financial_table')
        verbose_name = 'داده مالی پروژه'
        verbose_name_plural = 'داده‌های مالی پروژه'

    def __str__(self):
        return f"{self.project.title} - {self.financial_table.name}"


class FinanceSnapshot(models.Model):
    """عکس‌ فوری از داده‌های مالی پروژه برای گزارش یا نسخه‌گیری."""

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='finance_snapshots',
        verbose_name='پروژه'
    )
    snapshot_data = models.JSONField(verbose_name='داده عکس‌فوری')
    description = models.CharField(
        max_length=255,
        verbose_name='توضیحات',
        blank=True,
        null=True,
    )
    created_at = jmodels.jDateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'عکس‌فوری مالی'
        verbose_name_plural = 'عکس‌فوری‌های مالی'

    def __str__(self):
        return f"{self.project.title} - {self.created_at}"


class FinancialFormula(models.Model):
    """فرمول‌های محاسباتی پویا که می‌توانند در سطح جدول، فصل یا کل پروژه اعمال شوند."""

    LEVEL_CHOICES = (
        ('row', 'سطح ردیف'),
        ('table', 'سطح جدول'),
        ('section', 'سطح فصل'),
        ('project', 'کل طرح'),
    )

    financial_table = models.ForeignKey(
        FinancialTable,
        on_delete=models.CASCADE,
        related_name='formulas',
        verbose_name='جدول مالی',
        null=True,
        blank=True,
    )
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='table', verbose_name='سطح')
    result_key = models.CharField(max_length=100, verbose_name='کلید نتیجه')
    expression = models.TextField(verbose_name='عبارت فرمول')

    class Meta:
        verbose_name = 'فرمول مالی'
        verbose_name_plural = 'فرمول‌های مالی'
        unique_together = ('financial_table', 'result_key', 'level')

    def __str__(self):
        tbl = self.financial_table.name if self.financial_table else 'Global'
        return f"{tbl} - {self.result_key} ({self.level})" 