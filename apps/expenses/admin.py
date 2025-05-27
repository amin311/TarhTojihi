from django.contrib import admin
from .models import ExpenseCategory, Expense

@admin.register(ExpenseCategory)
class ExpenseCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('description', 'project', 'category', 'amount', 'unit', 'created_at', 'updated_at')
    list_filter = ('category', 'project')
    search_fields = ('description', 'project__title')
