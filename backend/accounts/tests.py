from allauth.account.models import EmailAddress
from django.test import TestCase


class RegistrationTest(TestCase):
    def test_admin_created_user(self):
        admin = User.objects.create_superuser('admin', 'admin@test.com', 'password')
        client = Client()
        client.login(username='admin', password='password')

        response = client.post('/admin/accounts/user/add/', {
            'username': 'newuser',
            'email': 'user@test.com',
            'password1': 'ComplexPass123!',
            'password2': 'ComplexPass123!',
            'role': 'CLIENT'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())