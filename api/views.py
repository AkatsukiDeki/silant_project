from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from core.models import Vehicle, Maintenance, Complaint
from .serializers import VehicleSerializer, MaintenanceSerializer, ComplaintSerializer
from core.filters import VehicleFilter, MaintenanceFilter, ComplaintFilter
from django_filters.rest_framework import DjangoFilterBackend

class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = VehicleFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.role == 'CLIENT':
            queryset = queryset.filter(client=self.request.user)
        elif self.request.user.role == 'SERVICE':
            queryset = queryset.filter(service_company=self.request.user)
        return queryset

class MaintenanceViewSet(viewsets.ModelViewSet):
    queryset = Maintenance.objects.all()
    serializer_class = MaintenanceSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = MaintenanceFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.role == 'CLIENT':
            queryset = queryset.filter(vehicle__client=self.request.user)
        elif self.request.user.role == 'SERVICE':
            queryset = queryset.filter(service_company=self.request.user)
        return queryset

class ComplaintViewSet(viewsets.ModelViewSet):
    queryset = Complaint.objects.all()
    serializer_class = ComplaintSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ComplaintFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.role == 'CLIENT':
            queryset = queryset.filter(vehicle__client=self.request.user)
        elif self.request.user.role == 'SERVICE':
            queryset = queryset.filter(service_company=self.request.user)
        return queryset