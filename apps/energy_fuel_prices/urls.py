# apps/energy_fuel_prices/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import energy_home, fueltype_list, price_setting_list
from .api import EnergyFuelTypeViewSet, RegionViewSet, PriceSettingViewSet

router = DefaultRouter()
router.register(r'energy-types', EnergyFuelTypeViewSet)
router.register(r'regions', RegionViewSet)
router.register(r'price-settings', PriceSettingViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('', energy_home, name='energy_home'),
    path('fueltypes/', fueltype_list, name='fueltype_list'),
    path('prices/', price_setting_list, name='price_setting_list'),
]
