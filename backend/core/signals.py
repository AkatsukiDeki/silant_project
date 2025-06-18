from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Maintenance, Complaint, LifecycleEvent

@receiver(post_save, sender=Maintenance)
def create_maintenance_event(sender, instance, created, **kwargs):
    if created:
        LifecycleEvent.objects.create(
            vehicle=instance.vehicle,
            event_type='MAINTENANCE',
            date=instance.date,
            operating_hours=instance.operating_hours,
            description=f'ТО: {instance.type.title} (Заказ-наряд {instance.order_number})'
        )

@receiver(post_save, sender=Complaint)
def create_complaint_event(sender, instance, created, **kwargs):
    if created:
        LifecycleEvent.objects.create(
            vehicle=instance.vehicle,
            event_type='COMPLAINT',
            date=instance.failure_date,
            operating_hours=instance.operating_hours,
            description=f'Отказ: {instance.failure_node.title} ({instance.recovery_method.title})'
        )