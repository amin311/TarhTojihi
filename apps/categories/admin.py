from django.contrib import admin
from .models import Category, Unit, FinancialTable, FinancialField

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ('name', 'symbol')
    search_fields = ('name', 'symbol')

@admin.register(FinancialTable)
class FinancialTableAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'description')
    list_filter = ('category',)
    search_fields = ('name', 'category__name')

@admin.register(FinancialField)
class FinancialFieldAdmin(admin.ModelAdmin):
    list_display = ('name', 'financial_table', 'field_type', 'unit')
    list_filter = ('field_type', 'financial_table')
    search_fields = ('name', 'financial_table__name')
