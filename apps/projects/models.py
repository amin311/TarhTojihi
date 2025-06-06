# apps/projects/models.py

from django.db import models
from django_jalali.db import models as jmodels
from apps.categories.models import Category
from apps.users.models import User
import json
from decimal import Decimal

class Project(models.Model):
    """
    اطلاعات اصلی هر پروژه (عنوان، توضیحات، نوع کسب‌وکار، مالک).
    """
    title = models.CharField(verbose_name='عنوان', max_length=255)
    description = models.TextField(verbose_name='توضیحات')
    business_type = models.ForeignKey(Category, verbose_name='نوع کسب و کار', on_delete=models.SET_NULL, null=True, related_name='projects')
    owner = models.ForeignKey(User, verbose_name='مالک', on_delete=models.CASCADE, related_name='projects')
    created_at = jmodels.jDateTimeField(verbose_name='تاریخ ایجاد', auto_now_add=True)
    updated_at = jmodels.jDateTimeField(verbose_name='تاریخ بروزرسانی', auto_now=True)

    class Meta:
        verbose_name = 'پروژه'
        verbose_name_plural = 'پروژه‌ها'

    def __str__(self):
        return self.title


class ProjectVersion(models.Model):
    """
    نگهداری نسخه‌های مختلف پروژه برای بازگشت به نسخه‌های قبلی یا مقایسه تغییرات.
    """
    project = models.ForeignKey(Project, verbose_name='پروژه', on_delete=models.CASCADE, related_name='versions')
    version_number = models.PositiveIntegerField(verbose_name='شماره نسخه')
    data = models.JSONField(verbose_name='داده‌ها')
    created_at = jmodels.jDateTimeField(verbose_name='تاریخ ایجاد', auto_now_add=True)

    class Meta:
        unique_together = ('project', 'version_number')
        ordering = ['-version_number']
        verbose_name = 'نسخه پروژه'
        verbose_name_plural = 'نسخه‌های پروژه'

    def __str__(self):
        return f"{self.project.title} - نسخه {self.version_number}"

    @property
    def get_completion_percentage(self):
        total_steps = 2  # تعداد گام‌ها
        completed_steps = 0
        if self.title and self.description:
            completed_steps += 1
        if self.business_type:
            completed_steps += 1
        percentage = (completed_steps / total_steps) * 100
        return int(percentage)


class ProjectChapter(models.Model):
    """فصول مختلف پروژه (سرمایه گذاری ثابت، سرمایه در گردش، ...)"""
    
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='chapters')
    title = models.CharField(max_length=200, verbose_name='عنوان فصل')
    order = models.PositiveIntegerField(verbose_name='ترتیب', default=1)
    description = models.TextField(blank=True, null=True, verbose_name='توضیحات')
    
    class Meta:
        unique_together = ('project', 'order')
        ordering = ['order']
        verbose_name = 'فصل پروژه'
        verbose_name_plural = 'فصول پروژه'
    
    def __str__(self):
        return f"{self.project.title} - {self.title}"


class DynamicTable(models.Model):
    """جداول پویا برای هر فصل"""
    
    chapter = models.ForeignKey(ProjectChapter, on_delete=models.CASCADE, related_name='tables')
    name = models.CharField(max_length=200, verbose_name='نام جدول')
    order = models.PositiveIntegerField(verbose_name='ترتیب', default=1)
    
    class Meta:
        unique_together = ('chapter', 'order')
        ordering = ['order']
        verbose_name = 'جدول پویا'
        verbose_name_plural = 'جداول پویا'
    
    def __str__(self):
        return f"{self.chapter.title} - {self.name}"


class TableColumn(models.Model):
    """ستون‌های هر جدول"""
    
    COLUMN_TYPES = (
        ('text', 'متن'),
        ('number', 'عدد'),
        ('calculated', 'محاسباتی'),
        ('reference', 'ارجاع'),
    )
    
    table = models.ForeignKey(DynamicTable, on_delete=models.CASCADE, related_name='columns')
    name = models.CharField(max_length=100, verbose_name='نام ستون')
    column_type = models.CharField(max_length=20, choices=COLUMN_TYPES, verbose_name='نوع ستون')
    order = models.PositiveIntegerField(verbose_name='ترتیب')
    unit = models.CharField(max_length=50, blank=True, null=True, verbose_name='واحد')
    formula = models.TextField(blank=True, null=True, verbose_name='فرمول محاسبه')
    
    class Meta:
        unique_together = ('table', 'order')
        ordering = ['order']
        verbose_name = 'ستون جدول'
        verbose_name_plural = 'ستون‌های جدول'


class TableRow(models.Model):
    """ردیف‌های هر جدول"""
    
    table = models.ForeignKey(DynamicTable, on_delete=models.CASCADE, related_name='rows')
    order = models.PositiveIntegerField(verbose_name='ترتیب')
    label = models.CharField(max_length=200, verbose_name='برچسب ردیف')
    
    class Meta:
        unique_together = ('table', 'order')
        ordering = ['order']
        verbose_name = 'ردیف جدول'
        verbose_name_plural = 'ردیف‌های جدول'


class CellValue(models.Model):
    """مقادیر سلول‌ها"""
    
    row = models.ForeignKey(TableRow, on_delete=models.CASCADE, related_name='cells')
    column = models.ForeignKey(TableColumn, on_delete=models.CASCADE, related_name='cells')
    value = models.TextField(verbose_name='مقدار')
    calculated_value = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, verbose_name='مقدار محاسبه شده')
    
    class Meta:
        unique_together = ('row', 'column')
        verbose_name = 'مقدار سلول'
        verbose_name_plural = 'مقادیر سلول‌ها'


class CalculationFormula(models.Model):
    """فرمول‌های محاسباتی پیشرفته"""
    
    SCOPE_CHOICES = (
        ('cell', 'سلول'),
        ('row', 'ردیف'),
        ('column', 'ستون'),
        ('table', 'جدول'),
        ('chapter', 'فصل'),
        ('cross_chapter', 'بین فصول'),
    )
    
    name = models.CharField(max_length=100, verbose_name='نام فرمول')
    scope = models.CharField(max_length=20, choices=SCOPE_CHOICES, verbose_name='قلمرو')
    formula = models.TextField(verbose_name='فرمول')
    description = models.TextField(blank=True, null=True, verbose_name='توضیحات')
    
    # ارجاعات
    source_table = models.ForeignKey(DynamicTable, on_delete=models.CASCADE, related_name='source_formulas', null=True, blank=True)
    target_table = models.ForeignKey(DynamicTable, on_delete=models.CASCADE, related_name='target_formulas', null=True, blank=True)
    source_column = models.ForeignKey(TableColumn, on_delete=models.CASCADE, related_name='source_formulas', null=True, blank=True)
    target_column = models.ForeignKey(TableColumn, on_delete=models.CASCADE, related_name='target_formulas', null=True, blank=True)
    
    class Meta:
        verbose_name = 'فرمول محاسباتی'
        verbose_name_plural = 'فرمول‌های محاسباتی'


class CalculationCache(models.Model):
    """کش محاسبات برای بهینه‌سازی"""
    
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='calculation_cache')
    cache_key = models.CharField(max_length=200, verbose_name='کلید کش')
    cached_value = models.JSONField(verbose_name='مقدار کش شده')
    last_updated = jmodels.jDateTimeField(auto_now=True, verbose_name='آخرین بروزرسانی')
    
    class Meta:
        unique_together = ('project', 'cache_key')
        verbose_name = 'کش محاسبات'
        verbose_name_plural = 'کش محاسبات'