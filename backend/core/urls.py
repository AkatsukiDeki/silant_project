from django.urls import path
from .views import (
    home, VehicleListView, VehicleDetailView,
    MaintenanceListView, MaintenanceCreateView,
    ComplaintListView, ComplaintCreateView, vehicle_search
)

urlpatterns = [
    path('', home, name='home'),
    path('vehicles/', VehicleListView.as_view(), name='vehicle-list'),
    path('vehicles/<int:pk>/', VehicleDetailView.as_view(), name='vehicle-detail'),
    path('maintenance/', MaintenanceListView.as_view(), name='maintenance-list'),
    path('maintenance/create/', MaintenanceCreateView.as_view(), name='maintenance-create'),
    path('complaints/', ComplaintListView.as_view(), name='complaint-list'),
    path('complaints/create/', ComplaintCreateView.as_view(), name='complaint-create'),
    path('search/', vehicle_search, name='vehicle-search'),
]