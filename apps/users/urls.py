# apps/users/urls.py

from django.urls import path
from . import views
from .api import RegisterView

urlpatterns = [
    path('', views.users_home, name='users_home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile_view'),
    path('register/', RegisterView.as_view(), name='register'),
]
