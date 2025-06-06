from rest_framework import viewsets, permissions
from .models import ProjectFinancialData, FinanceSnapshot, FinancialFormula
from .serializers import ProjectFinancialDataSerializer, FinanceSnapshotSerializer, FinancialFormulaSerializer


class ProjectFinancialDataViewSet(viewsets.ModelViewSet):
    queryset = ProjectFinancialData.objects.all()
    serializer_class = ProjectFinancialDataSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = self.queryset
        project_id = self.request.query_params.get('project')
        if project_id:
            qs = qs.filter(project_id=project_id)
        table_id = self.request.query_params.get('financial_table')
        if table_id:
            qs = qs.filter(financial_table_id=table_id)
        return qs


class FinanceSnapshotViewSet(viewsets.ModelViewSet):
    queryset = FinanceSnapshot.objects.all()
    serializer_class = FinanceSnapshotSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        project_id = self.request.query_params.get('project')
        if project_id:
            return self.queryset.filter(project_id=project_id)
        return self.queryset


# ---- Formula Viewset ----


class FinancialFormulaViewSet(viewsets.ModelViewSet):
    queryset = FinancialFormula.objects.all()
    serializer_class = FinancialFormulaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = self.queryset
        table_id = self.request.query_params.get('financial_table')
        if table_id:
            qs = qs.filter(financial_table_id=table_id)
        level = self.request.query_params.get('level')
        if level:
            qs = qs.filter(level=level)
        return qs 