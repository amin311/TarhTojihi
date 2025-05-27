# apps/categories/views.py

from django.shortcuts import render
from django.http import HttpResponse
from .models import Category, Unit, FinancialTable, FinancialField

def categories_home(request):
    """صفحه‌ی اصلی مدیریت دسته‌بندی‌ها."""
    return HttpResponse("مدیریت دسته‌بندی و جداول مالی")

def category_list(request):
    cats = Category.objects.all()
    return render(request, 'categories/category_list.html', {'categories': cats})
