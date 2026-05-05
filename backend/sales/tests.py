from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from unittest.mock import MagicMock, patch
from django.db import IntegrityError

from sales.models import Sale, SaleItem, Payment
from inventory.models import Product, Category
from businesses.models import Business
from customers.models import Customer


class SalesAPITestCase(TestCase):
    def setUp(self):
        self.user = get_user_model()()
        self.user.id = 1
        self.user.business_id = MagicMock()
        self.user.business_id.id = 1
        self.user.first_name = 'Test'
        
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
            sku='TEST001',
            cost_price=10.00,
            sell_price=20.00,
            stock=100,
            min_stock=10
        )
        
        self.customer = Customer.objects.create(
            business_id=self.business,
            name='Test Customer',
            phone='04121234567',
            identification_number='V12345678'
        )

    def test_list_sales(self):
        Sale.objects.create(
            business_id=self.business,
            customer_id=self.customer,
            user_id=MagicMock(id=1),
            subtotal=100.00,
            discount=0,
            tax=16.00,
            total=116.00,
            status='completed'
        )
        
        response = self.client.get('/api/sales/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)

    def test_create_sale_with_sufficient_stock(self):
        data = {
            'customer': self.customer.id,
            'subtotal': 40.00,
            'discount': 0,
            'tax': 6.40,
            'total': 46.40,
            'items': [
                {
                    'product': self.product.id,
                    'quantity': 2,
                    'unit_price': 20.00,
                    'total_price': 40.00
                }
            ]
        }
        
        response = self.client.post('/api/sales/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 98)

    def test_create_sale_with_insufficient_stock(self):
        self.product.stock = 1
        self.product.save()
        
        data = {
            'customer': self.customer.id,
            'subtotal': 60.00,
            'discount': 0,
            'tax': 9.60,
            'total': 69.60,
            'items': [
                {
                    'product': self.product.id,
                    'quantity': 10,
                    'unit_price': 20.00,
                    'total_price': 200.00
                }
            ]
        }
        
        response = self.client.post('/api/sales/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('errors', response.json())

    def test_sale_business_isolation(self):
        other_business = MagicMock()
        other_business.id = 999
        
        Sale.objects.create(
            business_id=other_business,
            customer_id=self.customer,
            user_id=MagicMock(id=1),
            subtotal=100.00,
            discount=0,
            tax=16.00,
            total=116.00,
            status='completed'
        )
        
        response = self.client.get('/api/sales/')
        self.assertEqual(len(response.json()), 0)


class SaleStockDeductionTestCase(TestCase):
    def setUp(self):
        self.business = Business(id=1, name='Test Business')
        self.business.id = 1
        
        self.category = Category.objects.create(
            business_id=self.business, name='Category')
        
        self.product = Product.objects.create(
            business_id=self.business,
            category_id=self.category,
            name='Product',
            sku='TEST001',
            cost_price=10.00,
            sell_price=20.00,
            stock=50,
            min_stock=10
        )
        
        self.customer = Customer.objects.create(
            business_id=self.business,
            name='Customer',
            phone='04121234567',
            identification_number='V12345678'
        )

    def test_stock_deducted_after_sale(self):
        initial_stock = self.product.stock
        
        sale = Sale.objects.create(
            business_id=self.business,
            customer_id=self.customer,
            user_id=MagicMock(id=1),
            subtotal=40.00,
            discount=0,
            tax=6.40,
            total=46.40,
            status='completed'
        )
        
        SaleItem.objects.create(
            sale_id=sale,
            product_id=self.product,
            quantity=5,
            unit_price=20.00,
            total_price=100.00
        )
        
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, initial_stock - 5)

    def test_multiple_items_stock_deduction(self):
        product2 = Product.objects.create(
            business_id=self.business,
            category_id=self.category,
            name='Product 2',
            sku='TEST002',
            cost_price=15.00,
            sell_price=30.00,
            stock=30,
            min_stock=5
        )
        
        sale = Sale.objects.create(
            business_id=self.business,
            customer_id=self.customer,
            user_id=MagicMock(id=1),
            subtotal=100.00,
            discount=0,
            tax=16.00,
            total=116.00,
            status='completed'
        )
        
        SaleItem.objects.create(sale_id=sale, product_id=self.product, quantity=3, unit_price=20.00, total_price=60.00)
        SaleItem.objects.create(sale_id=sale, product_id=product2, quantity=2, unit_price=30.00, total_price=60.00)
        
        self.product.refresh_from_db()
        product2.refresh_from_db()
        
        self.assertEqual(self.product.stock, 47)
        self.assertEqual(product2.stock, 28)


class PaymentTestCase(TestCase):
    def setUp(self):
        self.business = Business(id=1, name='Test Business')
        self.business.id = 1
        
        self.category = Category.objects.create(business_id=self.business, name='Category')
        
        self.customer = Customer.objects.create(
            business_id=self.business,
            name='Customer',
            phone='04121234567',
            identification_number='V12345678'
        )
        
        self.sale = Sale.objects.create(
            business_id=self.business,
            customer_id=self.customer,
            user_id=MagicMock(id=1),
            subtotal=100.00,
            discount=0,
            tax=16.00,
            total=116.00,
            status='pending'
        )

    def test_create_payment(self):
        payment = Payment.objects.create(
            sale_id=self.sale,
            method='cash',
            amount=116.00,
            reference='',
            status='completed'
        )
        
        self.assertEqual(payment.method, 'cash')
        self.assertEqual(float(payment.amount), 116.00)

    def test_payment_unique_reference_per_sale(self):
        Payment.objects.create(
            sale_id=self.sale,
            method='cash',
            amount=116.00,
            reference='REF001',
            status='completed'
        )
        
        with self.assertRaises(IntegrityError):
            Payment.objects.create(
                sale_id=self.sale,
                method='card',
                amount=116.00,
                reference='REF001',
                status='completed'
            )


class SaleItemModelTestCase(TestCase):
    def setUp(self):
        self.business = Business(id=1, name='Test Business')
        self.business.id = 1
        
        self.category = Category.objects.create(business_id=self.business, name='Category')
        
        self.product = Product.objects.create(
            business_id=self.business,
            category_id=self.category,
            name='Product',
            sku='TEST001',
            cost_price=10.00,
            sell_price=20.00,
            stock=50,
            min_stock=10
        )
        
        self.customer = Customer.objects.create(
            business_id=self.business,
            name='Customer',
            phone='04121234567',
            identification_number='V12345678'
        )
        
        self.sale = Sale.objects.create(
            business_id=self.business,
            customer_id=self.customer,
            user_id=MagicMock(id=1),
            subtotal=100.00,
            discount=0,
            tax=16.00,
            total=116.00,
            status='completed'
        )

    def test_sale_item_creation(self):
        item = SaleItem.objects.create(
            sale_id=self.sale,
            product_id=self.product,
            quantity=5,
            unit_price=20.00,
            total_price=100.00
        )
        
        self.assertEqual(item.quantity, 5)
        self.assertEqual(float(item.total_price), 100.00)

    def test_sale_item_unique_product_per_sale(self):
        SaleItem.objects.create(
            sale_id=self.sale,
            product_id=self.product,
            quantity=1,
            unit_price=20.00,
            total_price=20.00
        )
        
        with self.assertRaises(IntegrityError):
            SaleItem.objects.create(
                sale_id=self.sale,
                product_id=self.product,
                quantity=2,
                unit_price=20.00,
                total_price=40.00
            )