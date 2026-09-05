from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()

class AuthAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('auth-register')
        self.login_url = reverse('auth-login')
        self.admin_login_url = reverse('auth-admin-login')
        self.admin_register_url = reverse('auth-admin-register')
        self.me_url = reverse('auth-me')
        self.logout_url = reverse('auth-logout')

    def test_register_user(self):
        payload = {
            'name': 'Test User',
            'email': 'test@example.com',
            'password': 'password123',
            'mobile_number': '9876543210'
        }
        response = self.client.post(self.register_url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('token', response.data)
        self.assertEqual(response.data['user']['email'], 'test@example.com')
        self.assertEqual(response.data['user']['mobile_number'], '9876543210')

    def test_login_user(self):
        user = User.objects.create_user(
            username='loginuser',
            email='login@example.com',
            password='password123',
            name='Login User'
        )
        payload = {
            'email': 'login@example.com',
            'password': 'password123'
        }
        response = self.client.post(self.login_url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_admin_login(self):
        # Create regular customer
        customer = User.objects.create_user(
            username='normuser',
            email='norm@example.com',
            password='password123',
            is_staff=False
        )
        # Create staff admin
        admin = User.objects.create_user(
            username='adminuser',
            email='admin@example.com',
            password='password123',
            is_staff=True
        )

        # Attempting admin login with regular customer should fail (403 Forbidden)
        res_customer = self.client.post(self.admin_login_url, {'email': 'norm@example.com', 'password': 'password123'})
        self.assertEqual(res_customer.status_code, status.HTTP_403_FORBIDDEN)

        # Attempting admin login with admin user should succeed
        res_admin = self.client.post(self.admin_login_url, {'email': 'admin@example.com', 'password': 'password123'})
        self.assertEqual(res_admin.status_code, status.HTTP_200_OK)
        self.assertIn('token', res_admin.data)
        self.assertTrue(res_admin.data['user']['is_admin'])

    def test_admin_register(self):
        admin = User.objects.create_user(
            username='superadmin',
            email='superadmin@example.com',
            password='password123',
            is_staff=True,
            is_superuser=True
        )
        login_res = self.client.post(self.admin_login_url, {'email': 'superadmin@example.com', 'password': 'password123'})
        token = login_res.data['token']

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        new_admin_payload = {
            'name': 'Secondary Admin',
            'email': 'newadmin@example.com',
            'password': 'adminpassword123',
            'mobile_number': '9111111111'
        }
        res = self.client.post(self.admin_register_url, new_admin_payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(res.data['user']['is_staff'])

    def test_get_me_profile(self):
        user = User.objects.create_user(
            username='meuser',
            email='me@example.com',
            password='password123',
            name='Me User',
            addresses=[{"type": "Home", "city": "Jaipur"}]
        )
        login_res = self.client.post(self.login_url, {'email': 'me@example.com', 'password': 'password123'})
        token = login_res.data['token']

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.get(self.me_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'me@example.com')
        self.assertEqual(len(response.data['addresses']), 1)

