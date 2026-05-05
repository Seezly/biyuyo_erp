from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from unittest.mock import patch, MagicMock

from inventory.models import Category, Product, InventoryMovement
from businesses.models import Business


class InventoryAPITestCase(TestCase):
    def setUp(self):
        self.user = get_user_model()()
        self.user.id = 1
        self.user.business_id = MagicMock()
        self.user.business_id.id = 1
        
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        
        self.business = Business(id=1, name='Test Business')
        self.business.id = 1
        
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

    def test_create_product(self):
        data = {
            'name': 'New Product',
            'category': self.category.id,
            'description': 'New Description',
            'sku': 'NEW001',
            'cost_price': 15.00,
            'sell_price': 30.00,
            'stock': 50,
            'min_stock': 5
        }
        response = self.client.post('/api/products/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 2)

    def test_product_business_isolation(self):
        other_business = Business(id=999, name='Other Business')
        other_business.id = 999
        
        Product.objects.create(
            business_id=other_business,
            category_id=self.category,
            name='Other Business Product',
            sku='OTHER001',
            cost_price=10.00,
            sell_price=20.00,
            stock=10,
            min_stock=5
        )
        
        response = self.client.get('/api/products/')
        products = response.json()
        self.assertEqual(len(products), 1)
        self.assertEqual(products[0]['name'], 'Test Product')

    def test_list_categories(self):
        response = self.client.get('/api/categories/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_category(self):
        data = {'name': 'New Category'}
        response = self.client.post('/api/categories/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class InventorySignalsTestCase(TestCase):
    def setUp(self):
        self.business = Business(id=1, name='Test Business')
        self.business.id = 1
        
        self.category = Category.objects.create(
            business_id=self.business,
            name='Test Category'
        )

    def test_initial_stock_movement_creation(self):
        product = Product.objects.create(
            business_id=self.business,
            category_id=self.category,
            name='Product with Stock',
            sku='STOCK001',
            cost_price=10.00,
            sell_price=20.00,
            stock=50,
            min_stock=10
        )
        
        movements = InventoryMovement.objects.filter(product_id=product)
        self.assertTrue(movements.exists())
        movement = movements.first()
        self.assertEqual(movement.type, 'in')
        self.assertEqual(movement.quantity, 50)

    def test_stock_adjustment_movement(self):
        product = Product.objects.create(
            business_id=self.business,
            category_id=self.category,
            name='Product Adjustment',
            sku='ADJ001',
            cost_price=10.00,
            sell_price=20.00,
            stock=50,
            min_stock=10
        )
        
        product.stock = 60
        product.save()
        
        movements = InventoryMovement.objects.filter(product_id=product).count()
        self.assertEqual(movements, 2)

    def test_no_movement_when_stock_unchanged(self):
        product = Product.objects.create(
            business_id=self.business,
            category_id=self.category,
            name='Product Same',
            sku='SAME001',
            cost_price=10.00,
            sell_price=20.00,
            stock=50,
            min_stock=10
        )
        
        initial_count = InventoryMovement.objects.count()
        
        product.name = 'Updated Name'
        product.save()
        
        self.assertEqual(InventoryMovement.objects.count(), initial_count + 1)


class ProductModelTestCase(TestCase):
    def setUp(self):
        self.business = Business(id=1, name='Test Business')
        self.business.id = 1
        
        self.category = Category.objects.create(
            business_id=self.business,
            name='Test Category'
        )

    def test_product_creation(self):
        product = Product.objects.create(
            business_id=self.business,
            category_id=self.category,
            name='Test Product',
            sku='TEST001',
            cost_price=10.00,
            sell_price=20.00,
            stock=100,
            min_stock=10
        )
        self.assertEqual(str(product), 'Test Product')
        self.assertEqual(product.stock, 100)

    def test_product_unique_sku_per_business(self):
        Product.objects.create(
            business_id=self.business,
            category_id=self.category,
            name='Product 1',
            sku='UNIQUE001',
            cost_price=10.00,
            sell_price=20.00,
            stock=10,
            min_stock=5
        )
        
        with self.assertRaises(Exception):
            Product.objects.create(
                business_id=self.business,
                category_id=self.category,
                name='Product 2',
                sku='UNIQUE001',
                cost_price=15.00,
                sell_price=25.00,
                stock=20,
                min_stock=5
            )