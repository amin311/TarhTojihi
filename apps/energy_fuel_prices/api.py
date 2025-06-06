from rest_framework import viewsets, permissions
from .models import EnergyFuelType, Region, PriceSetting
from .serializers import EnergyFuelTypeSerializer, RegionSerializer, PriceSettingSerializer


class EnergyFuelTypeViewSet(viewsets.ModelViewSet):
    queryset = EnergyFuelType.objects.all()
    serializer_class = EnergyFuelTypeSerializer
    permission_classes = [permissions.IsAuthenticated]


class RegionViewSet(viewsets.ModelViewSet):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer
    permission_classes = [permissions.IsAuthenticated]


class PriceSettingViewSet(viewsets.ModelViewSet):
    queryset = PriceSetting.objects.select_related('energy_fuel_type', 'region', 'business_type').all()
    serializer_class = PriceSettingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        energy_type = self.request.query_params.get('energy_fuel_type')
        if energy_type:
            return self.queryset.filter(energy_fuel_type_id=energy_type)
        return self.queryset 