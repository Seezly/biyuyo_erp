from sales.models import Sale, SaleItem, Payment
from rest_framework import permissions, viewsets
from rest_framework.exceptions import PermissionDenied

from sales.serializers import SaleSerializer, SaleItemSerializer, PaymentSerializer


class SaleViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows sales to be viewed or edited.
    """

    serializer_class = SaleSerializer

    def get_queryset(self):
        user = self.request.user
        return Sale.objects.filter(business_id=user.business_id)

    def perform_create(self, serializer):
        serializer.save(business_id=self.request.user.business_id, user_id=self.request.user)

    def get_object(self):
        obj = super().get_object()
        if obj.business_id != self.request.user.business_id:
            raise PermissionDenied("No tienes acceso a esta venta.")
        return obj


class SaleItemViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows sale items to be viewed or edited.
    """

    serializer_class = SaleItemSerializer

    def get_queryset(self):
        user = self.request.user
        return SaleItem.objects.filter(sale_id__business_id=user.business_id)

    def get_object(self):
        obj = super().get_object()
        if obj.sale_id.business_id != self.request.user.business_id:
            raise PermissionDenied("No tienes acceso a este item.")
        return obj


class PaymentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows payments to be viewed or edited.
    """

    serializer_class = PaymentSerializer

    def get_queryset(self):
        user = self.request.user
        return Payment.objects.filter(sale_id__business_id=user.business_id)

    def get_object(self):
        obj = super().get_object()
        if obj.sale_id.business_id != self.request.user.business_id:
            raise PermissionDenied("No tienes acceso a este pago.")
        return obj
