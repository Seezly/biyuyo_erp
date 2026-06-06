from django.test import TestCase
from rest_framework import status

from test_helpers import (
    create_business, create_user, create_admin_user,
    get_authenticated_client,
)


class BusinessViewSetTestCase(TestCase):
    def setUp(self):
        self.business = create_business()
        self.user = create_user(self.business)
        self.client = get_authenticated_client(self.user)

    def test_list_businesses(self):
        response = self.client.get("/api/businesses/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_business_isolation(self):
        other = create_business(
            name="Other Business", rif="J000000001",
            phone="04120000001", email="other@test.com",
        )
        response = self.client.get("/api/businesses/")
        results = response.data.get("results", response.data)
        ids = [b["id"] for b in results]
        self.assertIn(self.business.id, ids)
        self.assertNotIn(other.id, ids)

    def test_get_own_business(self):
        response = self.client.get(f"/api/businesses/{self.business.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Test Business")

    def test_get_other_business_forbidden(self):
        other = create_business(
            name="Other", rif="J000000002",
            phone="04120000002", email="other2@test.com",
        )
        response = self.client.get(f"/api/businesses/{other.id}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_business(self):
        response = self.client.post(
            "/api/businesses/",
            {
                "name": "New Business",
                "description": "New",
                "rif": "J111111111",
                "address": "Addr",
                "state": "State",
                "municipality": "Muni",
                "phone": "04121111111",
                "email": "new@test.com",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class BusinessModelTestCase(TestCase):
    def test_str(self):
        business = create_business()
        self.assertEqual(str(business), "Test Business")

    def test_bool(self):
        business = create_business()
        self.assertTrue(bool(business))

    def test_get_owner(self):
        business = create_business()
        user = create_admin_user(business)
        owner = business.get_owner()
        self.assertIsNotNone(owner)
        self.assertEqual(owner.id, user.id)

    def test_get_users(self):
        business = create_business()
        create_user(business)
        users = business.get_users()
        self.assertEqual(users.count(), 1)

    def test_get_customers(self):
        from test_helpers import create_customer
        business = create_business()
        create_customer(business)
        customers = business.get_customers()
        self.assertEqual(customers.count(), 1)
