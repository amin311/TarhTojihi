from rest_framework import serializers
from .models import ProjectFinancialData, FinanceSnapshot


class ProjectFinancialDataSerializer(serializers.ModelSerializer):
    computed_metrics = serializers.JSONField(read_only=True)

    class Meta:
        model = ProjectFinancialData
        fields = '__all__'


class FinanceSnapshotSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinanceSnapshot
        fields = '__all__' 