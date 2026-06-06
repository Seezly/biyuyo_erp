import requests
from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny


class ExchangeRateView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        cached = cache.get("bcv_exchange_rate")
        if cached:
            return Response(cached)

        try:
            response = requests.get(
                "https://pydolarve.org/api/v1/dollar",
                timeout=10,
            )
            response.raise_for_status()
            data = response.json()

            usd_value = data.get("dollar", {}).get("price", 0)

            result = {
                "currency": "USD",
                "rate": usd_value,
                "source": "BCV",
            }

            cache.set("bcv_exchange_rate", result, timeout=3600)
            return Response(result)
        except Exception:
            fallback = {"currency": "USD", "rate": 500, "source": "fallback"}
            return Response(fallback)
