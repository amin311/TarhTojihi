from rest_framework import viewsets, permissions, filters
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
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class UnitViewSet(viewsets.ModelViewSet):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class FinancialTableViewSet(viewsets.ModelViewSet):
    queryset = FinancialTable.objects.select_related('category').all()
    serializer_class = FinancialTableSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.OrderingFilter]
    ordering = ['id']

    def get_queryset(self):
        qs = super().get_queryset()
        category_id = self.request.query_params.get('category')
        if category_id:
            qs = qs.filter(category_id=category_id)
        section = self.request.query_params.get('section')
        if section:
            qs = qs.filter(section=section)
        return qs


class FinancialFieldViewSet(viewsets.ModelViewSet):
    queryset = FinancialField.objects.select_related('financial_table').all()
    serializer_class = FinancialFieldSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly] 