# apps/categories/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.categories_home, name='categories_home'),
    path('list/', views.category_list, name='category_list'),
]
