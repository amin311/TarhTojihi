# apps/recommendations/models.py

from django.db import models
from apps.projects.models import Project

class Recommendation(models.Model):
    """
    پیشنهاد طرح‌های مشابه برای هر پروژه
    """
    project = models.ForeignKey(
        Project, 
        on_delete=models.CASCADE, 
        related_name='recommendations',
        verbose_name='پروژه'
    )
    similar_projects = models.ManyToManyField(
        Project, 
        related_name='recommended_for',
        verbose_name='پروژه‌های مشابه'
    )
    score = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        verbose_name='امتیاز'
    )

    def __str__(self):
        return f"Recommendation for {self.project.title}"
    
    class Meta:
        verbose_name = 'پیشنهاد'
        verbose_name_plural = 'پیشنهادات'
