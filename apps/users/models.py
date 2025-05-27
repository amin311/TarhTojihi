# apps/users/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """
    مدل سفارشی کاربر، که از AbstractUser ارث می‌برد.
    """
    ROLE_CHOICES = (
        ('admin', 'مدیر'),
        ('user', 'کاربر'),
    )
    role = models.CharField(verbose_name='نقش', max_length=10, choices=ROLE_CHOICES, default='user')

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'

    def __str__(self):
        return self.username


class Profile(models.Model):
    """
    نگهداری اطلاعات پروفایل کاربران، به صورت یک‌به‌یک با مدل User.
    """
    user = models.OneToOneField(User, verbose_name='کاربر', on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(verbose_name='نام کامل', max_length=100)
    phone_number = models.CharField(verbose_name='شماره تلفن', max_length=20, blank=True, null=True)
    address = models.TextField(verbose_name='آدرس', blank=True, null=True)

    class Meta:
        verbose_name = 'پروفایل'
        verbose_name_plural = 'پروفایل‌ها'

    def __str__(self):
        return f"Profile of {self.user.username}"
