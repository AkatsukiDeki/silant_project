import django_filters
from .models import Vehicle, Maintenance, Complaint

class VehicleFilter(django_filters.FilterSet):
    technique_model = django_filters.CharFilter(field_name='technique_model__title', label='Модель техники')
    engine_model = django_filters.CharFilter(field_name='engine_model__title', label='Модель двигателя')
    transmission_model = django_filters.CharFilter(field_name='transmission_model__title', label='Модель трансмиссии')
    driving_bridge_model = django_filters.CharFilter(field_name='driving_bridge_model__title', label='Модель ведущего моста')
    controlled_bridge_model = django_filters.CharFilter(field_name='controlled_bridge_model__title', label='Модель управляемого моста')

    class Meta:
        model = Vehicle
        fields = {
            'factory_number': ['exact'],
            'shipment_date': ['exact', 'gte', 'lte'],
        }

class MaintenanceFilter(django_filters.FilterSet):
    type = django_filters.CharFilter(field_name='type__title', label='Вид ТО')
    vehicle = django_filters.CharFilter(field_name='vehicle__factory_number', label='Зав. № машины')
    service_company = django_filters.CharFilter(field_name='service_company__username', label='Сервисная компания')

    class Meta:
        model = Maintenance
        fields = ['date', 'operating_hours']

class ComplaintFilter(django_filters.FilterSet):
    failure_node = django_filters.CharFilter(field_name='failure_node__title', label='Узел отказа')
    recovery_method = django_filters.CharFilter(field_name='recovery_method__title', label='Способ восстановления')
    vehicle = django_filters.CharFilter(field_name='vehicle__factory_number', label='Зав. № машины')

    class Meta:
        model = Complaint
        fields = ['failure_date', 'recovery_date']