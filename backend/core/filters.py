import django_filters
from .models import Vehicle, Maintenance, Complaint

class VehicleFilter(django_filters.FilterSet):
    class Meta:
        model = Vehicle
        fields = {
            'technique_model__title': ['exact'],
            'engine_model__title': ['exact'],
            'transmission_model__title': ['exact'],
            'driving_bridge_model__title': ['exact'],
            'controlled_bridge_model__title': ['exact'],
        }

class MaintenanceFilter(django_filters.FilterSet):
    class Meta:
        model = Maintenance
        fields = {
            'type__title': ['exact'],
            'vehicle__factory_number': ['exact'],
            'service_company__username': ['exact'],
        }

class ComplaintFilter(django_filters.FilterSet):
    class Meta:
        model = Complaint
        fields = {
            'failure_node__title': ['exact'],
            'recovery_method__title': ['exact'],
            'service_company__username': ['exact'],
        }