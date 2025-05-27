# apps/expenses/views.py

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Expense, ExpenseCategory

def expenses_home(request):
    """صفحه‌ی اصلی مدیریت هزینه‌ها."""
    return HttpResponse("مدیریت هزینه‌ها")

def expense_list(request):
    """فهرست هزینه‌ها."""
    exp = Expense.objects.select_related('project', 'category').all()
    return render(request, 'expenses/expense_list.html', {'expenses': exp})

def expense_detail(request, pk):
    """جزئیات یک هزینه."""
    expense = get_object_or_404(Expense, pk=pk)
    return render(request, 'expenses/expense_detail.html', {'expense': expense})
