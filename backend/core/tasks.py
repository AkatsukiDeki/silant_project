from celery import shared_task
from django.core.mail import send_mail
from .models import Vehicle

@shared_task
def notify_maintenance(vehicle_id):
    vehicle = Vehicle.objects.get(pk=vehicle_id)
    send_mail(
        'Требуется ТО',
        f'Машина {vehicle.factory_number} требует обслуживания к {vehicle.next_maintenance_date}',
        'noreply@silant.ru',
        [vehicle.client.email],
    )