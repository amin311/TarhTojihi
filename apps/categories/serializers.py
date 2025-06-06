# apps/categories/serializers.py

from rest_framework import serializers
from .models import Category, Unit, FinancialTable, FinancialField

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']

class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = ['id', 'name', 'symbol']

class FinancialFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialField
        fields = ['id', 'name', 'field_type', 'unit', 'order']

class FinancialTableSerializer(serializers.ModelSerializer):
    fields = FinancialFieldSerializer(many=True, read_only=True)

    class Meta:
        model = FinancialTable
        fields = ['id', 'name', 'description', 'category', 'section', 'table_type', 'fields']
