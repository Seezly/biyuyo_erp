from django.test import TestCase
from rest_framework import status

from accounts.models import CustomUser, ReminderSettings
from test_helpers import (
    create_business, create_user, create_admin_user,
    get_authenticated_client,
)


class UserViewSetTestCase(TestCase):
    def setUp(self):
        self.business = create_business()
        self.user = create_user(self.business)
        self.client = get_authenticated_client(self.user)

    def test_list_users(self):
        response = self.client.get("/api/users/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_isolation(self):
        other_business = create_business(
            name="Other", rif="J000000001", phone="04120000001", email="other@test.com"
        )
        create_user(other_business, email="other@test.com", phone="04120000002", identification_number="V00000001")
        response = self.client.get("/api/users/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data.get("results", response.data)
        for user_data in results:
            self.assertNotEqual(user_data.get("email"), "other@test.com")

    def test_me_endpoint(self):
        response = self.client.get("/api/me/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], self.user.email)

    def test_me_unauthenticated(self):
        from rest_framework.test import APIClient
        client = APIClient()
        response = client.get("/api/me/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_change_password(self):
        response = self.client.post(
            "/api/users/change-password/",
            {"current_password": "testpass123", "new_password": "newpass456"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_change_password_wrong_current(self):
        response = self.client.post(
            "/api/users/change-password/",
            {"current_password": "wrongpassword", "new_password": "newpass456"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_change_password_missing_fields(self):
        response = self.client.post(
            "/api/users/change-password/", {}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class RegisterViewTestCase(TestCase):
    def test_register_success(self):
        from rest_framework.test import APIClient
        client = APIClient()
        response = client.post(
            "/api/register/",
            {
                "email": "newowner@test.com",
                "first_name": "New",
                "last_name": "Owner",
                "identification_number": "V99999999",
                "phone": "04129999999",
                "password": "testpass123",
                "business_name": "New Business",
                "business_description": "A new business",
                "business_rif": "J999999999",
                "business_address": "123 Main St",
                "business_state": "Lara",
                "business_municipality": "Barquisimeto",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_register_missing_fields(self):
        from rest_framework.test import APIClient
        client = APIClient()
        response = client.post("/api/register/", {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LoginViewTestCase(TestCase):
    def setUp(self):
        self.business = create_business()
        self.user = create_user(self.business)

    def test_login_success(self):
        from rest_framework.test import APIClient
        client = APIClient()
        response = client.post(
            "/api/login/",
            {"email": "test@test.com", "password": "testpass123"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access_token", response.cookies)
        self.assertIn("refresh_token", response.cookies)

    def test_login_invalid_credentials(self):
        from rest_framework.test import APIClient
        client = APIClient()
        response = client.post(
            "/api/login/",
            {"email": "test@test.com", "password": "wrongpassword"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class LogoutViewTestCase(TestCase):
    def test_logout(self):
        from rest_framework.test import APIClient
        client = APIClient()
        response = client.post("/api/logout/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ReminderSettingsModelTestCase(TestCase):
    def test_create_reminder_settings(self):
        business = create_business()
        settings = ReminderSettings.objects.create(business_id=business)
        self.assertFalse(settings.whatsapp_enabled)
        self.assertFalse(settings.preventive_enabled)
        self.assertTrue("nombre" in settings.message_template)

    def test_str(self):
        business = create_business(name="Mi Negocio")
        settings = ReminderSettings.objects.create(business_id=business)
        self.assertIn("Mi Negocio", str(settings))
