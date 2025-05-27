# apps/expenses/models.py

from django.db import models
from django_jalali.db import models as jmodels
from apps.projects.models import Project
from apps.categories.models import Unit
# در صورت نیاز به دسته‌بندی هزینه‌ها:
# از apps.expenses.models import ExpenseCategory

class ExpenseCategory(models.Model):
    """
    دسته‌بندی‌های مختلف هزینه‌ها (استهلاک، تعمیرات، مواد اولیه و ...).
    """
    name = models.CharField(verbose_name='نام', max_length=100)
    description = models.TextField(verbose_name='توضیحات', blank=True, null=True)

    class Meta:
        verbose_name = 'دسته‌بندی هزینه'
        verbose_name_plural = 'دسته‌بندی‌های هزینه'

    def __str__(self):
        return self.name


class Expense(models.Model):
    """
    هزینه‌های مختلف مرتبط با پروژه‌ها، شامل مقدار هزینه، درصد استهلاک و ...
    """
    project = models.ForeignKey(Project, verbose_name='پروژه', on_delete=models.CASCADE, related_name='expenses')
    category = models.ForeignKey(ExpenseCategory, verbose_name='دسته‌بندی', on_delete=models.SET_NULL, null=True)
    description = models.CharField(verbose_name='توضیحات', max_length=255)
    percentage = models.DecimalField(verbose_name='درصد', max_digits=5, decimal_places=2, blank=True, null=True)
    amount = models.DecimalField(verbose_name='مقدار', max_digits=15, decimal_places=2)
    unit = models.ForeignKey(Unit, verbose_name='واحد', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = jmodels.jDateTimeField(auto_now_add=True)
    updated_at = jmodels.jDateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'هزینه'
        verbose_name_plural = 'هزینه‌ها'

    def __str__(self):
        return f"{self.description} - {self.amount} {self.unit}"
