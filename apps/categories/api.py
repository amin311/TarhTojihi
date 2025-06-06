from rest_framework import viewsets, permissions
from .models import Category, Unit, FinancialTable, FinancialField
from .serializers import (
    CategorySerializer,
    UnitSerializer,
    FinancialTableSerializer,
    FinancialFieldSerializer,
)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]


class UnitViewSet(viewsets.ModelViewSet):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer
    permission_classes = [permissions.IsAuthenticated]


class FinancialTableViewSet(viewsets.ModelViewSet):
    queryset = FinancialTable.objects.select_related('category').all()
    serializer_class = FinancialTableSerializer
    permission_classes = [permissions.IsAuthenticated]


class FinancialFieldViewSet(viewsets.ModelViewSet):
    queryset = FinancialField.objects.select_related('financial_table').all()
    serializer_class = FinancialFieldSerializer
    permission_classes = [permissions.IsAuthenticated] 