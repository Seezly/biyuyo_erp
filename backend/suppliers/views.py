from suppliers.models import Supplier, Purchase, PurchaseItem
from rest_framework import permissions, viewsets

from suppliers.serializers import (
    SupplierSerializer,
    PurchaseSerializer,
    PurchaseItemSerializer,
)


class SupplierViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows suppliers to be viewed or edited.
    """

    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [permissions.IsAuthenticated]


class PurchaseViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows purchase orders to be viewed or edited.
    """

    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer
    permission_classes = [permissions.IsAuthenticated]


class PurchaseItemViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows purchase items to be viewed or edited.
    """

    queryset = PurchaseItem.objects.all()
    serializer_class = PurchaseItemSerializer
    permission_classes = [permissions.IsAuthenticated]
