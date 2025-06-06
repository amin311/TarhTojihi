from rest_framework import viewsets, permissions
from .models import ProjectFinancialData, FinanceSnapshot
from .serializers import ProjectFinancialDataSerializer, FinanceSnapshotSerializer


class ProjectFinancialDataViewSet(viewsets.ModelViewSet):
    queryset = ProjectFinancialData.objects.all()
    serializer_class = ProjectFinancialDataSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # فیلتر بر اساس پروژه در صورت وجود پارامتر
        project_id = self.request.query_params.get('project')
        if project_id:
            return self.queryset.filter(project_id=project_id)
        return self.queryset


class FinanceSnapshotViewSet(viewsets.ModelViewSet):
    queryset = FinanceSnapshot.objects.all()
    serializer_class = FinanceSnapshotSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        project_id = self.request.query_params.get('project')
        if project_id:
            return self.queryset.filter(project_id=project_id)
        return self.queryset 