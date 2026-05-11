from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from django.db import IntegrityError

from sales.models import Sale, SaleItem, Payment
from inventory.models import Product, Category
from businesses.models import Business
from customers.models import Customer

User = get_user_model()


class SalesAPITestCase(TestCase):
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
            sku='TEST001',
            cost_price=10.00,
            sell_price=20.00,
            stock=100,
            min_stock=10
        )
        
        self.customer = Customer.objects.create(
            business_id=self.business,
            name='Test Customer',
            phone='1234567890',
            identification_number='V87654321'
        )

    def test_list_sales(self):
        Sale.objects.create(
            business_id=self.business,
            user_id=self.user,
            customer_id=self.customer,
            subtotal=100.00,
            discount=0.00,
            tax=0.00,
            total=100.00,
            status='completed'
        )
        
        response = self.client.get('/api/sales/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Handle paginated response
        results = response.data.get('results', response.data)
        self.assertGreaterEqual(len(results), 1)


class PaymentTestCase(TestCase):
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
        
        self.customer = Customer.objects.create(
            business_id=self.business,
            name='Test Customer',
            phone='1234567890',
            identification_number='V87654321'
        )
        
        self.sale = Sale.objects.create(
            business_id=self.business,
            user_id=self.user,
            customer_id=self.customer,
            subtotal=100.00,
            discount=0.00,
            tax=0.00,
            total=100.00,
            status='completed'
        )

    def test_create_payment(self):
        payment = Payment.objects.create(
            sale_id=self.sale,
            method='cash',
            amount=100.00,
            reference='CASH001',
            status='completed'
        )
        
        self.assertEqual(payment.amount, 100.00)
        self.assertEqual(payment.method, 'cash')


class SaleItemModelTestCase(TestCase):
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
            phone='1234567890',
            identification_number='V87654321'
        )
        
        self.sale = Sale.objects.create(
            business_id=self.business,
            user_id=self.user,
            customer_id=self.customer,
            subtotal=40.00,
            discount=0.00,
            tax=0.00,
            total=40.00,
            status='completed'
        )

    def test_sale_item_creation(self):
        item = SaleItem.objects.create(
            sale_id=self.sale,
            product_id=self.product,
            quantity=2,
            unit_price=20.00,
            total_price=40.00
        )
        
        self.assertEqual(item.quantity, 2)
        self.assertEqual(float(item.total_price), 40.00)

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