from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import permissions, viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework import status

from sales.models import Sale, SaleItem, Payment
from sales.serializers import SaleSerializer, SaleItemSerializer, PaymentSerializer
from inventory.models import Product


class SaleViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows sales to be viewed or edited.
    Includes stock validation and automatic stock deduction.
    """

    serializer_class = SaleSerializer

    def get_queryset(self):
        user = self.request.user
        return Sale.objects.filter(business_id=user.business_id)

    def create(self, request, *args, **kwargs):
        data = request.data
        items_data = data.get('items', [])

        errors = []
        for item in items_data:
            product_id = item.get('product')
            quantity = item.get('quantity', 0)

            if product_id and quantity > 0:
                try:
                    product = Product.objects.get(id=product_id, business_id=request.user.business_id)
                    if product.stock is not None and product.stock < quantity:
                        errors.append(f"Stock insuficiente para '{product.name}'. Disponible: {product.stock}, solicitado: {quantity}")
                except Product.DoesNotExist:
                    errors.append(f"Producto con ID {product_id} no encontrado")

        if errors:
            return Response({'errors': errors}, status=status.HTTP_400_BAD_REQUEST)

        return super().create(request, *args, **kwargs)

    @transaction.atomic
    def perform_create(self, serializer):
        request = self.context.get('request')
        items_data = request.data.get('items', []) if request else []

        sale = serializer.save(
            business_id=request.user.business_id,
            user_id=request.user
        )

        for item_data in items_data:
            product_id = item_data.get('product')
            quantity = item_data.get('quantity', 0)

            if product_id and quantity > 0:
                try:
                    product = Product.objects.get(id=product_id, business_id=request.user.business_id)

                    SaleItem.objects.create(
                        sale_id=sale,
                        product_id=product,
                        quantity=quantity,
                        unit_price=item_data.get('unit_price', float(product.sell_price)),
                        total_price=item_data.get('total_price', float(product.sell_price) * quantity)
                    )

                    if product.stock is not None:
                        product.stock -= quantity
                        product.save()
                except Product.DoesNotExist:
                    pass

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
