from django.test import TestCase
from rest_framework import status

from test_helpers import (
    create_business, create_user, create_supplier, create_product,
    create_category, get_authenticated_client,
)
from suppliers.models import Purchase, PurchaseItem


class SupplierViewSetTestCase(TestCase):
    def setUp(self):
        self.business = create_business()
        self.user = create_user(self.business)
        self.client = get_authenticated_client(self.user)

    def test_list_suppliers(self):
        create_supplier(self.business)
        response = self.client.get("/api/suppliers/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_supplier(self):
        response = self.client.post(
            "/api/suppliers/",
            {
                "name": "New Supplier",
                "rif": "J111111111",
                "email": "new@supplier.com",
                "address": "123 Street",
                "phone": "04123334455",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_supplier_isolation(self):
        other = create_business(
            name="Other", rif="J000000001",
            phone="04120000001", email="other@test.com",
        )
        create_supplier(other, rif="J000000099", phone="04120000099", email="s@other.com")
        response = self.client.get("/api/suppliers/")
        results = response.data.get("results", response.data)
        self.assertEqual(len(results), 0)


class PurchaseViewSetTestCase(TestCase):
    def setUp(self):
        self.business = create_business()
        self.user = create_user(self.business)
        self.client = get_authenticated_client(self.user)
        self.supplier = create_supplier(self.business)

    def test_list_purchases(self):
        Purchase.objects.create(
            business_id=self.business,
            supplier_id=self.supplier,
            total=500.00,
        )
        response = self.client.get("/api/purchases/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_purchase(self):
        response = self.client.post(
            "/api/purchases/",
            {"supplier_id": self.supplier.id, "total": "100.00", "status": "pending"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class PurchaseItemViewSetTestCase(TestCase):
    def setUp(self):
        self.business = create_business()
        self.user = create_user(self.business)
        self.client = get_authenticated_client(self.user)
        self.supplier = create_supplier(self.business)
        self.category = create_category(self.business)
        self.product = create_product(self.business, self.category)
        self.purchase = Purchase.objects.create(
            business_id=self.business,
            supplier_id=self.supplier,
            total=500.00,
        )

    def test_list_purchase_items(self):
        PurchaseItem.objects.create(
            purchase_id=self.purchase,
            product_id=self.product,
            quantity=10,
            cost_price=5.00,
            total_price=50.00,
        )
        response = self.client.get("/api/purchase-items/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class SupplierModelTestCase(TestCase):
    def test_str(self):
        business = create_business()
        supplier = create_supplier(business, name="Acme Corp")
        self.assertEqual(str(supplier), "Acme Corp")

    def test_bool(self):
        business = create_business()
        supplier = create_supplier(business)
        self.assertTrue(bool(supplier))


class PurchaseModelTestCase(TestCase):
    def test_status_choices(self):
        business = create_business()
        supplier = create_supplier(business)
        purchase = Purchase.objects.create(
            business_id=business,
            supplier_id=supplier,
            total=100.00,
            status="completed",
        )
        self.assertEqual(purchase.status, "completed")
