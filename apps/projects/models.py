# apps/projects/models.py

from django.db import models
from django_jalali.db import models as jmodels
from apps.categories.models import Category
from apps.users.models import User

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