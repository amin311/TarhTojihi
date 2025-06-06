# apps/expenses/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .api import ExpenseCategoryViewSet, ExpenseViewSet

router = DefaultRouter()
router.register(r'expense-categories', ExpenseCategoryViewSet)
router.register(r'expenses', ExpenseViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('', views.expenses_home, name='expenses_home'),
    path('list/', views.expense_list, name='expense_list'),
    path('<int:pk>/', views.expense_detail, name='expense_detail'),
]
