# apps/users/urls.py

from django.urls import path
from .views import users_home, login_view, logout_view, profile_view

urlpatterns = [
    path('', users_home, name='users_home'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_view, name='profile_view'),
]
