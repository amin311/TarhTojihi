# apps/energy_fuel_prices/serializers.py

from rest_framework import serializers
from .models import EnergyFuelType, Region, PriceSetting

class EnergyFuelTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnergyFuelType
        fields = ['id', 'name', 'description']

class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ['id', 'name', 'description']

class PriceSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceSetting
        fields = ['id', 'energy_fuel_type', 'season', 'region', 'business_type', 'base_price', 'created_at', 'updated_at']
