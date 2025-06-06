# apps/projects/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    projects_home,
    project_list,
    project_detail,
    create_project_step1,
    create_project_step2,
)
from .api import ProjectViewSet, ProjectVersionViewSet

router = DefaultRouter()
router.register(r'projects', ProjectViewSet)
router.register(r'project-versions', ProjectVersionViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('', projects_home, name='projects_home'),  # نام URL: projects_home
    path('list/', project_list, name='project_list'),
    path('<int:pk>/', project_detail, name='project_detail'),
    path('create/step1/', create_project_step1, name='create_project_step1'),
    path('create/step2/<int:pk>/', create_project_step2, name='create_project_step2'),
]
