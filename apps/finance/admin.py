from django.contrib import admin
from .models import ProjectFinancialData, FinanceSnapshot, FinancialFormula


@admin.register(ProjectFinancialData)
class ProjectFinancialDataAdmin(admin.ModelAdmin):
    list_display = ('project', 'financial_table', 'updated_at')
    search_fields = ('project__title', 'financial_table__name')
    list_filter = ('financial_table',)


@admin.register(FinanceSnapshot)
class FinanceSnapshotAdmin(admin.ModelAdmin):
    list_display = ('project', 'created_at', 'description')
    search_fields = ('project__title', 'description')


@admin.register(FinancialFormula)
class FinancialFormulaAdmin(admin.ModelAdmin):
    list_display = ('financial_table', 'result_key', 'level')
    search_fields = ('result_key', 'financial_table__name')
    list_filter = ('level',) 