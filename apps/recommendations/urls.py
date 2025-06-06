# apps/recommendations/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .api import RecommendationViewSet

router = DefaultRouter()
router.register(r'recommendations', RecommendationViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('', views.recommendations_home, name='recommendations_home'),
    path('<int:project_id>/list/', views.recommendation_list, name='recommendation_list'),
]
