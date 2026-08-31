from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from apps.categories.models import Category
from .models import Product

User = get_user_model()

class ProductAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.category = Category.objects.create(name='Dairy / Milk', sector='DAIRY', description='Fresh dairy')
        self.product = Product.objects.create(
            sku='TEST-DAI-001',
            category=self.category,
            name='Milk 1L',
            description='Full cream milk',
            price=68.00,
            discount_price=65.00,
            unit='1 L',
            stock_quantity=500,
            is_available=True,
            is_active=True,
            tags=['daily-fresh'],
            attributes={'fat_content': '6.0%'}
        )
        self.admin_user = User.objects.create_superuser(
            username='adminprod',
            email='adminprod@test.com',
            password='password123'
        )

    def test_list_products(self):
        url = reverse('product-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['sku'], 'TEST-DAI-001')
        self.assertEqual(response.data[0]['unit'], '1 L')

    def test_filter_products_by_sector(self):
        url = f"{reverse('product-list')}?sector=DAIRY"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_filter_products_by_sku(self):
        url = f"{reverse('product-list')}?sku=TEST-DAI-001"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_search_products(self):
        url = f"{reverse('product-list')}?search=Milk"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_admin_create_product(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('admin-product-list-create')
        payload = {
            'sku': 'TEST-DAI-002',
            'category_id': self.category.id,
            'name': 'Paneer 200g',
            'description': 'Fresh malai paneer',
            'price': '120.00',
            'discount_price': '110.00',
            'unit': '200 g',
            'stock_quantity': 100,
            'tags': ['protein-rich'],
            'attributes': {'refrigeration_required': True}
        }
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 2)
