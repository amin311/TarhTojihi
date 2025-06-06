# apps/categories/models.py

from django.db import models

class Category(models.Model):
    """
    دسته‌بندی‌های مختلف کسب‌وکار (خدماتی، تولیدی، فناوری و ...).
    """
    name = models.CharField(verbose_name='نام', max_length=100)
    description = models.TextField(verbose_name='توضیحات', blank=True, null=True)

    class Meta:
        verbose_name = 'دسته‌بندی'
        verbose_name_plural = 'دسته‌بندی‌ها'

    def __str__(self):
        return self.name


class Unit(models.Model):
    """
    واحدهای اندازه‌گیری (مثلاً متر مربع، کیلوگرم، لیتر و ...).
    """
    name = models.CharField(verbose_name='نام', max_length=50)
    symbol = models.CharField(verbose_name='نماد', max_length=20, blank=True, null=True)

    class Meta:
        verbose_name = 'واحد'
        verbose_name_plural = 'واحدها'

    def __str__(self):
        return self.name


class FinancialTable(models.Model):
    """
    جداول مالی مرتبط با هر دسته‌بندی، مانند هزینه‌های جاری، استهلاک و ...
    """
    SECTION_CHOICES = (
        ('capex', 'سرمایه‌گذاری ثابت'),
        ('opex', 'هزینه‌های متغیر'),
        ('revenue', 'درآمد/فروش'),
        ('analysis', 'تحلیل و شاخص‌ها'),
    )
    TABLE_TYPE_CHOICES = (
        ('grid', 'جدولی'),
        ('text', 'متنی'),
        ('auto', 'خودکار'),
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='financial_tables', verbose_name='دسته‌بندی')
    name = models.CharField(verbose_name='نام', max_length=100)
    description = models.TextField(verbose_name='توضیحات', blank=True, null=True)
    section = models.CharField(max_length=20, choices=SECTION_CHOICES, default='capex', verbose_name='فصل')
    table_type = models.CharField(max_length=10, choices=TABLE_TYPE_CHOICES, default='grid', verbose_name='نوع جدول')

    def __str__(self):
        return f"{self.category.name} - {self.name}"


class FinancialField(models.Model):
    """
    فیلدهای مختلف (ستون‌ها) در هر جدول مالی.
    """
    order = models.PositiveIntegerField(verbose_name='ترتیب', default=0)
    FIELD_TYPE_CHOICES = (
        ('numeric', 'عدد'),
        ('text', 'متن'),
    )
    financial_table = models.ForeignKey(FinancialTable, on_delete=models.CASCADE, related_name='fields', verbose_name='جدول مالی')
    name = models.CharField(verbose_name='نام', max_length=100)
    field_type = models.CharField(verbose_name='نوع فیلد', max_length=50, choices=FIELD_TYPE_CHOICES)
    unit = models.ForeignKey(Unit, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='واحد')

    def __str__(self):
        return f"{self.financial_table.name} - {self.name}"

    class Meta:
        ordering = ['order', 'id']  # نمایش به ترتیب تعریف‌شده
