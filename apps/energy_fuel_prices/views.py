# apps/energy_fuel_prices/views.py
from django.shortcuts import render, get_object_or_404
from .models import EnergyFuelType, Region, PriceSetting

def energy_home(request):
    """صفحه‌ی اصلی مدیریت قیمت‌های انرژی."""
    return render(request, 'energy_fuel_prices/home.html')

def fueltype_list(request):
    """فهرست انواع سوخت و انرژی."""
    fuel_types = EnergyFuelType.objects.all()
    return render(request, 'energy_fuel_prices/fueltype_list.html', {'fuel_types': fuel_types})

def price_setting_list(request):
    """فهرست تنظیمات قیمت."""
    prices = PriceSetting.objects.select_related('energy_fuel_type', 'region', 'business_type').all()
    return render(request, 'energy_fuel_prices/prices_list.html', {'prices': prices})
