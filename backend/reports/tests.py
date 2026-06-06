from django.test import TestCase
from rest_framework import status

from test_helpers import (
    create_business, create_user, create_admin_user, create_product,
    create_category, create_sale, create_customer, create_supplier,
    get_authenticated_client,
)


class ReportSummaryTestCase(TestCase):
    def setUp(self):
        self.business = create_business()
        self.user = create_user(self.business)
        self.client = get_authenticated_client(self.user)
        self.category = create_category(self.business)
        self.product = create_product(self.business, self.category)
        self.customer = create_customer(self.business)

    def test_summary(self):
        response = self.client.get("/api/reports/summary/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertGreaterEqual(len(response.data), 1)

    def test_sales_report(self):
        create_sale(self.business, self.user, self.customer)
        response = self.client.get("/api/reports/sales/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("total_sales", response.data)
        self.assertIn("count", response.data)

    def test_inventory_report(self):
        response = self.client.get("/api/reports/inventory/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("total_products", response.data)
        self.assertIn("total_value", response.data)

    def test_customers_report(self):
        response = self.client.get("/api/reports/customers/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("total_customers", response.data)

    def test_global_stats_forbidden(self):
        response = self.client.get("/api/reports/global_stats/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_global_stats_admin(self):
        admin = create_admin_user(self.business)
        client = get_authenticated_client(admin)
        response = client.get("/api/reports/global_stats/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("totalBusinesses", response.data)
