# apps/users/views.py

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from .models import User

def users_home(request):
    """صفحه‌ی اصلی مدیریت کاربران (مثال ساده)."""
    return HttpResponse("مدیریت کاربران")

def login_view(request):
    """نمای ورود کاربر با فرض یک فرم ساده در قالب."""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('users_home')
        else:
            return HttpResponse("نام کاربری یا رمز عبور اشتباه است.")
    return render(request, 'users/login.html')

def logout_view(request):
    """خروج از حساب کاربری."""
    logout(request)
    return redirect('login')

def profile_view(request):
    """مشاهده‌ی پروفایل کاربر."""
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'users/profile.html', {"user": request.user})
