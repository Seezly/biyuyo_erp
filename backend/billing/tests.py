from django.test import TestCase
from rest_framework import status

from test_helpers import (
    create_business, create_user, create_admin_user, create_plan, create_subscription,
    get_authenticated_client,
)


class PlanViewSetTestCase(TestCase):
    def setUp(self):
        self.business = create_business()
        self.user = create_admin_user(self.business)
        self.client = get_authenticated_client(self.user)

    def test_list_plans(self):
        create_plan()
        response = self.client.get("/api/plans/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_plan(self):
        response = self.client.post(
            "/api/plans/",
            {"name": "Pro Plan", "price": 29.99, "max_users": 20, "max_products": 500},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_plan_requires_admin(self):
        regular = create_user(self.business)
        client = get_authenticated_client(regular)
        response = client.get("/api/plans/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class SubscriptionViewSetTestCase(TestCase):
    def setUp(self):
        self.business = create_business()
        self.user = create_user(self.business)
        self.client = get_authenticated_client(self.user)
        self.plan = create_plan()

    def test_list_subscriptions(self):
        create_subscription(self.business, self.plan)
        response = self.client.get("/api/subscriptions/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_subscription(self):
        response = self.client.post(
            "/api/subscriptions/",
            {
                "plan_id": self.plan.id,
                "status": "active",
                "start_date": "2025-01-01T00:00:00Z",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_subscription_isolation(self):
        other = create_business(
            name="Other", rif="J000000001",
            phone="04120000001", email="other@test.com",
        )
        create_subscription(other, self.plan)
        response = self.client.get("/api/subscriptions/")
        results = response.data.get("results", response.data)
        self.assertEqual(len(results), 0)


class PlanModelTestCase(TestCase):
    def test_str(self):
        plan = create_plan(name="Enterprise")
        self.assertEqual(str(plan), "Enterprise")

    def test_float(self):
        plan = create_plan(price=49.99)
        self.assertEqual(float(plan), 49.99)
