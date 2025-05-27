from django.contrib import admin
from .models import EnergyFuelType, Region, PriceSetting

@admin.register(EnergyFuelType)
class EnergyFuelTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(PriceSetting)
class PriceSettingAdmin(admin.ModelAdmin):
    list_display = ('energy_fuel_type', 'season', 'region', 'business_type', 'base_price', 'created_at', 'updated_at')
    list_filter = ('energy_fuel_type', 'season', 'region', 'business_type')
    search_fields = ('energy_fuel_type__name', 'region__name', 'business_type__name')
