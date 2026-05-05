from suppliers.models import Supplier, Purchase, PurchaseItem
from rest_framework import permissions, viewsets
from rest_framework.exceptions import PermissionDenied

from suppliers.serializers import (
    SupplierSerializer,
    PurchaseSerializer,
    PurchaseItemSerializer,
)


class SupplierViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows suppliers to be viewed or edited.
    """

    serializer_class = SupplierSerializer

    def get_queryset(self):
        user = self.request.user
        return Supplier.objects.filter(business_id=user.business_id)

    def perform_create(self, serializer):
        serializer.save(business_id=self.request.user.business_id)

    def get_object(self):
        obj = super().get_object()
        if obj.business_id != self.request.user.business_id:
            raise PermissionDenied("No tienes acceso a este proveedor.")
        return obj


class PurchaseViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows purchase orders to be viewed or edited.
    """

    serializer_class = PurchaseSerializer

    def get_queryset(self):
        user = self.request.user
        return Purchase.objects.filter(business_id=user.business_id)

    def perform_create(self, serializer):
        serializer.save(business_id=self.request.user.business_id)

    def get_object(self):
        obj = super().get_object()
        if obj.business_id != self.request.user.business_id:
            raise PermissionDenied("No tienes acceso a esta compra.")
        return obj


class PurchaseItemViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows purchase items to be viewed or edited.
    """

    serializer_class = PurchaseItemSerializer

    def get_queryset(self):
        user = self.request.user
        return PurchaseItem.objects.filter(purchase_id__business_id=user.business_id)

    def get_object(self):
        obj = super().get_object()
        if obj.purchase_id.business_id != self.request.user.business_id:
            raise PermissionDenied("No tienes acceso a este item de compra.")
        return obj
