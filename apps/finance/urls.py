from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProjectFinancialDataViewSet, FinanceSnapshotViewSet, FinancialFormulaViewSet

router = DefaultRouter()
router.register(r'project-financial-data', ProjectFinancialDataViewSet)
router.register(r'finance-snapshots', FinanceSnapshotViewSet)
router.register(r'formulas', FinancialFormulaViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
] 