from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = [
        ('CLIENT', 'Клиент'),
        ('SERVICE', 'Сервисная организация'),
        ('MANAGER', 'Менеджер'),
    ]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='CLIENT')
    company_name = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.get_full_name()} ({self.get_role_display()})"