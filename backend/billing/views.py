from billing.models import Plan, Subscription, Invoice
from rest_framework import permissions, viewsets
from rest_framework.exceptions import PermissionDenied

from billing.serializers import (
    PlanSerializer,
    SubscriptionSerializer,
    InvoiceSerializer,
)


class PlanViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows plans to be viewed or edited.
    Global for all businesses, admin only.
    """

    queryset = Plan.objects.all().order_by("name")
    serializer_class = PlanSerializer
    permission_classes = [permissions.IsAdminUser]


class SubscriptionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows subscriptions to be viewed or edited.
    """

    serializer_class = SubscriptionSerializer

    def get_queryset(self):
        user = self.request.user
        return Subscription.objects.filter(business_id=user.business_id).order_by("-start_date")

    def perform_create(self, serializer):
        serializer.save(business_id=self.request.user.business_id)

    def get_object(self):
        obj = super().get_object()
        if obj.business_id != self.request.user.business_id:
            raise PermissionDenied("No tienes acceso a esta suscripción.")
        return obj


class InvoiceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows invoices to be viewed or edited.
    """

    serializer_class = InvoiceSerializer

    def get_queryset(self):
        user = self.request.user
        return Invoice.objects.filter(subscription_id__business_id=user.business_id).order_by("-created_at")

    def get_object(self):
        obj = super().get_object()
        if obj.subscription_id.business_id != self.request.user.business_id:
            raise PermissionDenied("No tienes acceso a esta factura.")
        return obj
