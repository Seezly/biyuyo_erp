from django.test import TestCase
from rest_framework import status

from test_helpers import (
    create_business, create_user, create_customer,
    get_authenticated_client,
)


class CustomerViewSetTestCase(TestCase):
    def setUp(self):
        self.business = create_business()
        self.user = create_user(self.business)
        self.client = get_authenticated_client(self.user)

    def test_list_customers(self):
        create_customer(self.business)
        response = self.client.get("/api/customers/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_customer(self):
        response = self.client.post(
            "/api/customers/",
            {
                "name": "New Customer",
                "phone": "04123334455",
                "identification_number": "V11111111",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_customer_isolation(self):
        other = create_business(
            name="Other", rif="J000000001",
            phone="04120000001", email="other@test.com",
        )
        create_customer(other, phone="04120000002", identification_number="V00000001")
        response = self.client.get("/api/customers/")
        results = response.data.get("results", response.data)
        self.assertEqual(len(results), 0)

    def test_update_customer(self):
        customer = create_customer(self.business)
        response = self.client.patch(
            f"/api/customers/{customer.id}/",
            {"name": "Updated Name"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Updated Name")

    def test_delete_customer(self):
        customer = create_customer(self.business)
        response = self.client.delete(f"/api/customers/{customer.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class CustomerModelTestCase(TestCase):
    def test_str(self):
        business = create_business()
        customer = create_customer(business, name="Juan Perez")
        self.assertEqual(str(customer), "Juan Perez")

    def test_unique_constraint(self):
        business = create_business()
        create_customer(business, identification_number="V12345678")
        with self.assertRaises(Exception):
            create_customer(business, identification_number="V12345678", phone="04129999999")
