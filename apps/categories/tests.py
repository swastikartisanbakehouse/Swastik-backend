from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Category

User = get_user_model()

class CategoryAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.category = Category.objects.create(
            name='Bakery',
            sector='BAKERY',
            description='Fresh bakery goods',
            is_active=True,
            metadata={'supports_customization': True}
        )
        self.admin_user = User.objects.create_superuser(
            username='adminuser',
            email='admin@test.com',
            password='password123'
        )

    def test_list_categories(self):
        url = reverse('category-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['sector'], 'BAKERY')

    def test_admin_create_category(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('admin-category-create')
        payload = {
            'name': 'Sweets',
            'sector': 'SWEETS',
            'description': 'Tasty sweets',
            'metadata': {'weight_based_pricing': True}
        }
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 2)

    def test_unauthorized_user_cannot_create_category(self):
        url = reverse('admin-category-create')
        payload = {'name': 'Unauthorized', 'sector': 'DAIRY', 'description': 'Test'}
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
