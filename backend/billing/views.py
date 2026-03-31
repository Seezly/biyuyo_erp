from billing.models import Plan, Subscription, Invoice
from rest_framework import permissions, viewsets

from billing.serializers import (
    PlanSerializer,
    SubscriptionSerializer,
    InvoiceSerializer,
)


class PlanViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows plans to be viewed or edited.
    """

    queryset = Plan.objects.all().order_by("name")
    serializer_class = PlanSerializer
    permission_classes = [permissions.IsAdminUser]


class SubscriptionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows subscriptions to be viewed or edited.
    """

    queryset = Subscription.objects.all().order_by("-start_date")
    serializer_class = SubscriptionSerializer
    permission_classes = [permissions.IsAdminUser]


class InvoiceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows invoices to be viewed or edited.
    """

    queryset = Invoice.objects.all().order_by("-created_at")
    serializer_class = InvoiceSerializer
    permission_classes = [permissions.IsAdminUser]
