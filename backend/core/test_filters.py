from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from core.models import Vehicle

class FilterTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Создаем тестовые данные

    def test_vehicle_filters(self):
        url = reverse('api:vehicle-list')
        response = self.client.get(url + '?technique_model=Силант-100&engine_model=Д-260')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.data) > 0)