# apps/energy_fuel_prices/urls.py
from django.urls import path
from .views import energy_home, fueltype_list, price_setting_list

urlpatterns = [
    path('', energy_home, name='energy_home'),
    path('fueltypes/', fueltype_list, name='fueltype_list'),
    path('prices/', price_setting_list, name='price_setting_list'),
]
