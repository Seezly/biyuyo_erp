from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

from inventory.models import Category, Product, InventoryMovement
from businesses.models import Business

User = get_user_model()


class InventoryAPITestCase(TestCase):
    def setUp(self):
        self.business = Business.objects.create(name='Test Business', rif='J123456789')
        
        self.user = User.objects.create_user(
            first_name='Test',
            last_name='User',
            email='test@test.com',
            business_id=self.business,
            identification_number='V12345678',
            phone='1234567890',
            password='testpass123'
        )
        
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        
        self.category = Category.objects.create(
            business_id=self.business,
            name='Test Category'
        )
        
        self.product = Product.objects.create(
            business_id=self.business,
            category_id=self.category,
            name='Test Product',
            description='Test Description',
            sku='TEST001',
            cost_price=10.00,
            sell_price=20.00,
            stock=100,
            min_stock=10
        )

    def test_list_products(self):
        response = self.client.get('/api/products/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_categories(self):
        response = self.client.get('/api/categories/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Handle paginated response
        results = response.data.get('results', response.data)
        self.assertGreaterEqual(len(results), 1)


class InventorySignalsTestCase(TestCase):
    def setUp(self):
        self.business = Business.objects.create(name='Test Business', rif='J123456789')
        
        self.user = User.objects.create_user(
            first_name='Test',
            last_name='User',
            email='test@test.com',
            business_id=self.business,
            identification_number='V12345678',
            phone='1234567890',
            password='testpass123'
        )
        
        self.category = Category.objects.create(
            business_id=self.business,
            name='Test Category'
        )

    def test_initial_stock_movement_creation(self):
        product = Product.objects.create(
            business_id=self.business,
            category_id=self.category,
            name='Product With Stock',
            sku='STOCK001',
            cost_price=10.00,
            sell_price=20.00,
            stock=50,
            min_stock=10
        )
        
        movements = InventoryMovement.objects.filter(product_id=product)
        self.assertTrue(movements.exists())
        self.assertEqual(movements.first().type, 'in')


class ProductModelTestCase(TestCase):
    def setUp(self):
        self.business = Business.objects.create(name='Test Business', rif='J123456789')
        
        self.category = Category.objects.create(
            business_id=self.business,
            name='Test Category'
        )

    def test_product_creation(self):
        product = Product.objects.create(
            business_id=self.business,
            category_id=self.category,
            name='Model Test Product',
            sku='MODEL001',
            cost_price=15.00,
            sell_price=25.00,
            stock=75,
            min_stock=5
        )
        
        self.assertEqual(product.name, 'Model Test Product')
        self.assertEqual(product.stock, 75)

    def test_product_stock_property(self):
        product = Product.objects.create(
            business_id=self.business,
            category_id=self.category,
            name='Stock Test',
            sku='STOCKTEST001',
            cost_price=10.00,
            sell_price=15.00,
            stock=5,
            min_stock=10
        )
        
        self.assertEqual(product.stock, 5)
        self.assertEqual(product.min_stock, 10)