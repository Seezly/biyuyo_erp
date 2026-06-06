from unittest.mock import patch, MagicMock
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

from core.views import ExchangeRateView


class ExchangeRateViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    @patch("core.views.requests.get")
    def test_exchange_rate_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"dollar": {"price": 36.5}}
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        response = self.client.get("/api/exchange-rate/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["currency"], "USD")
        self.assertEqual(response.data["rate"], 36.5)
        self.assertEqual(response.data["source"], "BCV")

    @patch("core.views.requests.get")
    def test_exchange_rate_api_failure_returns_fallback(self, mock_get):
        mock_get.side_effect = Exception("Connection timeout")

        response = self.client.get("/api/exchange-rate/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["rate"], 500)
        self.assertEqual(response.data["source"], "fallback")

    def test_exchange_rate_unauthenticated(self):
        response = self.client.get("/api/exchange-rate/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
