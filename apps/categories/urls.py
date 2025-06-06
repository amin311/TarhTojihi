# apps/categories/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .api import CategoryViewSet, UnitViewSet, FinancialTableViewSet, FinancialFieldViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'units', UnitViewSet)
router.register(r'financial-tables', FinancialTableViewSet)
router.register(r'financial-fields', FinancialFieldViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('', views.categories_home, name='categories_home'),
    path('list/', views.category_list, name='category_list'),
]
