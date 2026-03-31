from sales.models import Sale, SaleItem, Payment
from rest_framework import permissions, viewsets

from sales.serializers import SaleSerializer, SaleItemSerializer, PaymentSerializer


class SaleViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows sales to be viewed or edited.
    """

    queryset = Sale.objects.all()
    serializer_class = SaleSerializer
    permission_classes = [permissions.IsAdminUser]


class SaleItemViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows sale items to be viewed or edited.
    """

    queryset = SaleItem.objects.all()
    serializer_class = SaleItemSerializer
    permission_classes = [permissions.IsAdminUser]


class PaymentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows payments to be viewed or edited.
    """

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAdminUser]
