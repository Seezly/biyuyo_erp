from django.test import TestCase
from rest_framework import status

from test_helpers import (
    create_business, create_user, create_admin_user,
    create_audit_log, get_authenticated_client,
)


class AuditLogListViewTestCase(TestCase):
    def setUp(self):
        self.business = create_business()
        self.user = create_admin_user(self.business)
        self.client = get_authenticated_client(self.user)

    def test_list_audit_logs(self):
        create_audit_log(self.user)
        response = self.client.get("/api/audit/logs/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_audit_log_isolation(self):
        other_business = create_business(
            name="Other", rif="J000000001",
            phone="04120000001", email="other@test.com",
        )
        other_user = create_user(other_business, email="other@test.com", phone="04120000002", identification_number="V00000001")
        create_audit_log(other_user)
        response = self.client.get("/api/audit/logs/")
        results = response.data.get("results", response.data)
        for log in results:
            self.assertNotEqual(log.get("email"), "other@test.com")


class AuditLogDetailViewTestCase(TestCase):
    def setUp(self):
        self.business = create_business()
        self.user = create_admin_user(self.business)
        self.client = get_authenticated_client(self.user)

    def test_get_audit_log_detail(self):
        log = create_audit_log(self.user)
        response = self.client.get(f"/api/audit/logs/{log.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_nonexistent_audit_log(self):
        response = self.client.get("/api/audit/logs/99999/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class AuditLogModelTestCase(TestCase):
    def test_str_with_user(self):
        business = create_business()
        user = create_user(business)
        log = create_audit_log(user, action="create", model_name="Product")
        self.assertIn(user.email, str(log))
        self.assertIn("create", str(log))

    def test_str_without_user(self):
        from audit.models import AuditLog
        log = AuditLog.objects.create(
            action="login",
            model_name="Session",
            description="User logged in",
        )
        self.assertIn("Anonymous", str(log))
