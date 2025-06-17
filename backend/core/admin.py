from django.contrib import admin
from .models import Vehicle, Maintenance, Complaint, Reference
from django.contrib.auth.models import Group

class VehicleAdmin(admin.ModelAdmin):
    list_display = ('serial_number', 'model', 'client', 'service_company', 'shipping_date')
    list_filter = ('model', 'engine_model', 'client', 'service_company')
    search_fields = ('serial_number', 'engine_serial', 'transmission_serial')
    readonly_fields = ('shipping_date',)
    fieldsets = (
        ('Основная информация', {
            'fields': ('serial_number', 'model', 'shipping_date')
        }),
        ('Комплектующие', {
            'fields': ('engine_model', 'engine_serial',
                      'transmission_model', 'transmission_serial',
                      'driving_axle_model', 'driving_axle_serial',
                      'steering_axle_model', 'steering_axle_serial')
        }),
        ('Дополнительно', {
            'fields': ('supply_contract', 'consignee',
                      'delivery_address', 'equipment',
                      'client', 'service_company')
        }),
    )

class MaintenanceAdmin(admin.ModelAdmin):
    list_display = ('vehicle', 'type', 'date', 'service_company')
    list_filter = ('type', 'service_company', 'date')
    search_fields = ('vehicle__serial_number', 'order_number')
    date_hierarchy = 'date'

class ComplaintAdmin(admin.ModelAdmin):
    list_display = ('vehicle', 'failure_node', 'failure_date', 'recovery_method', 'downtime_days')
    list_filter = ('failure_node', 'recovery_method', 'service_company')
    search_fields = ('vehicle__serial_number', 'failure_description')
    date_hierarchy = 'failure_date'

class ReferenceAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

# Регистрация моделей
admin.site.register(Vehicle, VehicleAdmin)
admin.site.register(Maintenance, MaintenanceAdmin)
admin.site.register(Complaint, ComplaintAdmin)
admin.site.register(Reference, ReferenceAdmin)

# Настройка заголовков админки
admin.site.site_header = "Администрирование сервиса Силант"
admin.site.site_title = "Сервис мониторинга Силант"
admin.site.index_title = "Управление данными"