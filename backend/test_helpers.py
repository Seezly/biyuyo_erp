from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework.test import APIClient

from businesses.models import Business
from customers.models import Customer
from inventory.models import Category, Product
from suppliers.models import Supplier
from billing.models import Plan, Subscription
from sales.models import Sale
from audit.models import AuditLog

User = get_user_model()


def create_business(**kwargs):
    defaults = {
        "name": "Test Business",
        "description": "Test Description",
        "rif": "J123456789",
        "address": "Test Address",
        "state": "Test State",
        "municipality": "Test Municipality",
        "phone": "04121234567",
        "email": "business@test.com",
    }
    defaults.update(kwargs)
    return Business.objects.create(**defaults)


def create_user(business, **kwargs):
    defaults = {
        "first_name": "Test",
        "last_name": "User",
        "email": "test@test.com",
        "business_id": business,
        "identification_number": "V12345678",
        "phone": "04121234568",
        "password": "testpass123",
    }
    defaults.update(kwargs)
    password = defaults.pop("password")
    user = User.objects.create_user(**defaults, password=password)
    return user


def create_admin_user(business, **kwargs):
    user = create_user(business, **kwargs)
    user.is_staff = True
    user.is_superuser = True
    user.save()
    owner_group, _ = Group.objects.get_or_create(name="owner")
    user.groups.add(owner_group)
    return user


def create_customer(business, **kwargs):
    defaults = {
        "business_id": business,
        "name": "Test Customer",
        "phone": "04129876543",
        "identification_number": "V87654321",
    }
    defaults.update(kwargs)
    return Customer.objects.create(**defaults)


def create_category(business, **kwargs):
    defaults = {"business_id": business, "name": "Test Category"}
    defaults.update(kwargs)
    return Category.objects.create(**defaults)


def create_product(business, category, **kwargs):
    defaults = {
        "business_id": business,
        "category_id": category,
        "name": "Test Product",
        "description": "Test Description",
        "sku": "TEST001",
        "cost_price": 10.00,
        "sell_price": 20.00,
        "stock": 100,
        "min_stock": 10,
    }
    defaults.update(kwargs)
    return Product.objects.create(**defaults)


def create_supplier(business, **kwargs):
    defaults = {
        "business_id": business,
        "name": "Test Supplier",
        "rif": "J987654321",
        "email": "supplier@test.com",
        "address": "Supplier Address",
        "phone": "04121112233",
    }
    defaults.update(kwargs)
    return Supplier.objects.create(**defaults)


def create_plan(**kwargs):
    defaults = {
        "name": "Basic Plan",
        "price": 9.99,
        "max_users": 5,
        "max_products": 100,
    }
    defaults.update(kwargs)
    return Plan.objects.create(**defaults)


def create_subscription(business, plan, **kwargs):
    from django.utils import timezone
    defaults = {
        "business_id": business,
        "plan_id": plan,
        "status": "active",
        "start_date": timezone.now(),
    }
    defaults.update(kwargs)
    return Subscription.objects.create(**defaults)


def create_sale(business, user, customer, **kwargs):
    defaults = {
        "business_id": business,
        "user_id": user,
        "customer_id": customer,
        "subtotal": 100.00,
        "discount": 0.00,
        "tax": 0.00,
        "total": 100.00,
        "status": "completed",
    }
    defaults.update(kwargs)
    return Sale.objects.create(**defaults)


def create_audit_log(user, **kwargs):
    defaults = {
        "user": user,
        "action": "create",
        "model_name": "TestModel",
        "object_id": "1",
        "object_repr": "Test Object",
        "description": "Test audit log",
    }
    defaults.update(kwargs)
    return AuditLog.objects.create(**defaults)


def get_authenticated_client(user):
    client = APIClient()
    client.force_authenticate(user=user)
    return client
