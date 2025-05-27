# apps/recommendations/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.recommendations_home, name='recommendations_home'),
    path('<int:project_id>/list/', views.recommendation_list, name='recommendation_list'),
]
