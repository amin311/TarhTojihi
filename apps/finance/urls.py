from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProjectFinancialDataViewSet, FinanceSnapshotViewSet

router = DefaultRouter()
router.register(r'project-financial-data', ProjectFinancialDataViewSet)
router.register(r'finance-snapshots', FinanceSnapshotViewSet)

urlpatterns = [
    path('', include(router.urls)),
] 