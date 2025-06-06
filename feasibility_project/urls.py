# feasibility_project/urls.py

from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/', include('apps.users.urls')),
    path('projects/', include('apps.projects.urls')),
    path('categories/', include('apps.categories.urls')),
    path('expenses/', include('apps.expenses.urls')),
    path('energy/', include('apps.energy_fuel_prices.urls')),
    path('recommendations/', include('apps.recommendations.urls')),
    path('finance/', include('apps.finance.urls')),
    path('', RedirectView.as_view(pattern_name='projects_home', permanent=False)),  # مسیر خالی به پروژه‌ها هدایت می‌شود
]
