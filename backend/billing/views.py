from billing.models import Plan, Subscription, Invoice
from rest_framework import permissions, viewsets
from rest_framework.exceptions import PermissionDenied

from core.mixins import FilteringMixin
from billing.serializers import (
    PlanSerializer,
    SubscriptionSerializer,
    InvoiceSerializer,
)


class PlanViewSet(FilteringMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows plans to be viewed or edited.
    Global for all businesses, admin only.
    """

    queryset = Plan.objects.all().order_by("name")
    serializer_class = PlanSerializer
    permission_classes = [permissions.IsAdminUser]
    search_fields = ['name']
    ordering_fields = ['name', 'price']
    default_ordering = ['name']

    def get_queryset(self):
        return super().get_queryset()


class SubscriptionViewSet(FilteringMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows subscriptions to be viewed or edited.
    """

    queryset = Subscription.objects.select_related('business_id', 'plan_id').all()
    serializer_class = SubscriptionSerializer
    search_fields = ['business_id__name', 'plan_id__name']
    filter_fields = ['status']
    ordering_fields = ['start_date', 'end_date', 'created_at']
    default_ordering = ['-start_date']

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(business_id=self.request.user.business_id)
        return self.filter_queryset_with_params(queryset)

    def perform_create(self, serializer):
        serializer.save(business_id=self.request.user.business_id)

    def get_object(self):
        obj = super().get_object()
        if obj.business_id != self.request.user.business_id:
            raise PermissionDenied("You do not have access to this subscription.")
        return obj


class InvoiceViewSet(FilteringMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows invoices to be viewed or edited.
    """

    queryset = Invoice.objects.select_related('subscription_id').all()
    serializer_class = InvoiceSerializer
    search_fields = ['subscription_id__business_id__name']
    filter_fields = ['status']
    ordering_fields = ['created_at', 'amount']
    default_ordering = ['-created_at']

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(subscription_id__business_id=self.request.user.business_id)
        return self.filter_queryset_with_params(queryset)

    def get_object(self):
        obj = super().get_object()
        if obj.subscription_id.business_id != self.request.user.business_id:
            raise PermissionDenied("You do not have access to this invoice.")
        return obj

    def perform_create(self, serializer):
        subscription = serializer.validated_data.get('subscription_id')
        if subscription and subscription.business_id != self.request.user.business_id:
            raise PermissionDenied("No tienes acceso a esta suscripción.")
        serializer.save()
