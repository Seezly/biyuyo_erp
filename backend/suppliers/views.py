from rest_framework import permissions, viewsets
from rest_framework.exceptions import PermissionDenied

from core.mixins import FilteringMixin
from suppliers.models import Supplier, Purchase, PurchaseItem
from suppliers.serializers import (
    SupplierSerializer,
    PurchaseSerializer,
    PurchaseItemSerializer,
)


class SupplierViewSet(FilteringMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows suppliers to be viewed or edited.
    Supports search by name/rif/phone, and ordering.
    """

    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    search_fields = ['name', 'rif', 'phone', 'email']
    filter_fields = []
    ordering_fields = ['name', 'created_at']
    default_ordering = ['-created_at']

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(business_id=self.request.user.business_id)
        return self.filter_queryset_with_params(queryset)

    def perform_create(self, serializer):
        serializer.save(business_id=self.request.user.business_id)

    def get_object(self):
        obj = super().get_object()
        if obj.business_id != self.request.user.business_id:
            raise PermissionDenied("You do not have access to this supplier.")
        return obj


class PurchaseViewSet(FilteringMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows purchase orders to be viewed or edited.
    Supports search by supplier name, filtering by status, and ordering.
    """

    queryset = Purchase.objects.select_related('supplier_id').all()
    serializer_class = PurchaseSerializer
    search_fields = ['id', 'supplier_id__name']
    filter_fields = ['status']
    ordering_fields = ['created_at', 'total']
    default_ordering = ['-created_at']

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(business_id=self.request.user.business_id)
        return self.filter_queryset_with_params(queryset)

    def perform_create(self, serializer):
        serializer.save(business_id=self.request.user.business_id)

    def get_object(self):
        obj = super().get_object()
        if obj.business_id != self.request.user.business_id:
            raise PermissionDenied("You do not have access to this purchase.")
        return obj


class PurchaseItemViewSet(FilteringMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows purchase items to be viewed or edited.
    """

    queryset = PurchaseItem.objects.select_related('purchase_id', 'product_id').all()
    serializer_class = PurchaseItemSerializer
    search_fields = ['product_id__name']
    filter_fields = ['purchase_id', 'product_id']
    ordering_fields = ['created_at', 'quantity']
    default_ordering = ['-created_at']

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(purchase_id__business_id=self.request.user.business_id)
        return self.filter_queryset_with_params(queryset)

    def get_object(self):
        obj = super().get_object()
        if obj.purchase_id.business_id != self.request.user.business_id:
            raise PermissionDenied("You do not have access to this purchase item.")
        return obj