from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Directory(models.Model):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title

class Vehicle(models.Model):
    factory_number = models.CharField(max_length=50, unique=True, verbose_name='Зав. № машины')
    technique_model = models.ForeignKey(
        Directory, on_delete=models.PROTECT,
        related_name='technique_models', verbose_name='Модель техники'
    )
    engine_model = models.ForeignKey(
        Directory, on_delete=models.PROTECT,
        related_name='engine_models', verbose_name='Модель двигателя'
    )
    engine_number = models.CharField(max_length=50, verbose_name='Зав. № двигателя')
    transmission_model = models.ForeignKey(
        Directory, on_delete=models.PROTECT,
        related_name='transmission_models', verbose_name='Модель трансмиссии'
    )
    transmission_number = models.CharField(max_length=50, verbose_name='Зав. № трансмиссии')
    driving_bridge_model = models.ForeignKey(
        Directory, on_delete=models.PROTECT,
        related_name='driving_bridge_models', verbose_name='Модель ведущего моста'
    )
    driving_bridge_number = models.CharField(max_length=50, verbose_name='Зав. № ведущего моста')
    controlled_bridge_model = models.ForeignKey(
        Directory, on_delete=models.PROTECT,
        related_name='controlled_bridge_models', verbose_name='Модель управляемого моста'
    )
    controlled_bridge_number = models.CharField(max_length=50, verbose_name='Зав. № управляемого моста')
    delivery_contract = models.CharField(max_length=100, verbose_name='Договор поставки №, дата')
    shipment_date = models.DateField(verbose_name='Дата отгрузки с завода')
    consignee = models.CharField(max_length=100, verbose_name='Грузополучатель')
    delivery_address = models.CharField(max_length=200, verbose_name='Адрес поставки')
    equipment = models.TextField(verbose_name='Комплектация')
    client = models.ForeignKey(
        User, on_delete=models.PROTECT,
        related_name='vehicles', verbose_name='Клиент'
    )
    service_company = models.ForeignKey(
        User, on_delete=models.PROTECT,
        related_name='serviced_vehicles', verbose_name='Сервисная компания'
    )

    next_maintenance_date = models.DateField(null=True, blank=True)
    maintenance_notified = models.BooleanField(default=False)

    def check_maintenance(self):
        if self.next_maintenance_date and self.next_maintenance_date <= timezone.now().date() + timezone.timedelta(
                days=7):
            if not self.maintenance_notified:
                from .tasks import notify_maintenance
                notify_maintenance.delay(self.pk)
                self.maintenance_notified = True
                self.save()

    class Meta:
        ordering = ['-shipment_date']
        verbose_name = 'Машина'
        verbose_name_plural = 'Машины'

    def __str__(self):
        return f"{self.technique_model} (№{self.factory_number})"

class Maintenance(models.Model):
    type = models.ForeignKey(
        Directory, on_delete=models.PROTECT,
        related_name='maintenance_types', verbose_name='Вид ТО'
    )
    date = models.DateField(verbose_name='Дата проведения ТО')
    operating_hours = models.PositiveIntegerField(verbose_name='Наработка, м/час')
    order_number = models.CharField(max_length=50, verbose_name='№ заказ-наряда')
    order_date = models.DateField(verbose_name='Дата заказ-наряда')
    service_company = models.ForeignKey(
        User, on_delete=models.PROTECT,
        related_name='maintenances', verbose_name='Сервисная компания'
    )
    vehicle = models.ForeignKey(
        Vehicle, on_delete=models.CASCADE,
        related_name='maintenances', verbose_name='Машина'
    )

    class Meta:
        ordering = ['-date']
        verbose_name = 'Техническое обслуживание'
        verbose_name_plural = 'Технические обслуживания'

    def __str__(self):
        return f"{self.type} для {self.vehicle}"

class Complaint(models.Model):
    failure_date = models.DateField(verbose_name='Дата отказа')
    operating_hours = models.PositiveIntegerField(verbose_name='Наработка, м/час')
    failure_node = models.ForeignKey(
        Directory, on_delete=models.PROTECT,
        related_name='failure_nodes', verbose_name='Узел отказа'
    )
    failure_description = models.TextField(verbose_name='Описание отказа')
    recovery_method = models.ForeignKey(
        Directory, on_delete=models.PROTECT,
        related_name='recovery_methods', verbose_name='Способ восстановления'
    )
    spare_parts = models.TextField(blank=True, verbose_name='Используемые запчасти')
    recovery_date = models.DateField(verbose_name='Дата восстановления')
    downtime = models.PositiveIntegerField(editable=False, verbose_name='Время простоя')
    vehicle = models.ForeignKey(
        Vehicle, on_delete=models.CASCADE,
        related_name='complaints', verbose_name='Машина'
    )
    service_company = models.ForeignKey(
        User, on_delete=models.PROTECT,
        related_name='complaints', verbose_name='Сервисная компания'
    )

    class Meta:
        ordering = ['-failure_date']
        verbose_name = 'Рекламация'
        verbose_name_plural = 'Рекламации'

    def save(self, *args, **kwargs):
        self.downtime = (self.recovery_date - self.failure_date).days
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Рекламация {self.vehicle} ({self.failure_node})"