from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Vehicle, Maintenance, Complaint
from .filters import VehicleFilter, MaintenanceFilter, ComplaintFilter


def home(request):
    return render(request, 'core/home.html')


class VehicleListView(LoginRequiredMixin, ListView):
    model = Vehicle
    template_name = 'core/vehicle_list.html'
    context_object_name = 'vehicles'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.role == 'CLIENT':
            queryset = queryset.filter(client=self.request.user)
        elif self.request.user.role == 'SERVICE':
            queryset = queryset.filter(service_company=self.request.user)

        self.filterset = VehicleFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class VehicleDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Vehicle
    template_name = 'core/vehicle_detail.html'
    context_object_name = 'vehicle'

    def test_func(self):
        vehicle = self.get_object()
        user = self.request.user
        return (
                user.role == 'MANAGER' or
                vehicle.client == user or
                vehicle.service_company == user
        )


class MaintenanceListView(LoginRequiredMixin, ListView):
    model = Maintenance
    template_name = 'core/maintenance_list.html'
    context_object_name = 'maintenances'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.role == 'CLIENT':
            queryset = queryset.filter(vehicle__client=self.request.user)
        elif self.request.user.role == 'SERVICE':
            queryset = queryset.filter(service_company=self.request.user)

        self.filterset = MaintenanceFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class MaintenanceCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Maintenance
    fields = ['type', 'date', 'operating_hours', 'order_number', 'order_date', 'vehicle']
    template_name = 'core/maintenance_form.html'

    def test_func(self):
        return self.request.user.role in ['MANAGER', 'SERVICE']

    def form_valid(self, form):
        form.instance.service_company = self.request.user
        return super().form_valid(form)


class ComplaintListView(LoginRequiredMixin, ListView):
    model = Complaint
    template_name = 'core/complaint_list.html'
    context_object_name = 'complaints'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.role == 'CLIENT':
            queryset = queryset.filter(vehicle__client=self.request.user)
        elif self.request.user.role == 'SERVICE':
            queryset = queryset.filter(service_company=self.request.user)

        self.filterset = ComplaintFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class ComplaintCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Complaint
    fields = ['failure_date', 'operating_hours', 'failure_node', 'failure_description',
              'recovery_method', 'spare_parts', 'recovery_date', 'vehicle']
    template_name = 'core/complaint_form.html'

    def test_func(self):
        return self.request.user.role in ['MANAGER', 'SERVICE']

    def form_valid(self, form):
        form.instance.service_company = self.request.user
        return super().form_valid(form)


def vehicle_search(request):
    if request.method == 'GET':
        factory_number = request.GET.get('factory_number')
        if factory_number:
            vehicle = Vehicle.objects.filter(factory_number=factory_number).first()
            if vehicle:
                return render(request, 'core/vehicle_guest_detail.html', {'vehicle': vehicle})
            return render(request, 'core/vehicle_search.html', {'error': 'Машина с таким номером не найдена'})
    return render(request, 'core/vehicle_search.html')