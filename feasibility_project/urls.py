# feasibility_project/urls.py

from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('apps.users.urls')),
    path('projects/', include('apps.projects.urls')),
    path('categories/', include('apps.categories.urls')),
    path('expenses/', include('apps.expenses.urls')),
    path('energy/', include('apps.energy_fuel_prices.urls')),
    path('recommendations/', include('apps.recommendations.urls')),
    path('', RedirectView.as_view(pattern_name='projects_home', permanent=False)),  # مسیر خالی به پروژه‌ها هدایت می‌شود
]
