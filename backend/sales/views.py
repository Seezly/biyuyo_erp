from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
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
        return Sale.objects.filter(business_id=user.business_id).prefetch_related('saleitem_set', 'payment_set')

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        sale_data = SaleSerializer(instance).data
        sale_data['items'] = SaleItemSerializer(instance.saleitem_set.all(), many=True).data
        sale_data['payments'] = PaymentSerializer(instance.payment_set.all(), many=True).data
        return Response(sale_data)

    @action(detail=True, methods=['get'])
    def receipt(self, request, pk=None):
        """Get sale details formatted for receipt"""
        sale = self.get_object()
        items = sale.saleitem_set.all()
        payments = sale.payment_set.all()

        from django.template.loader import render_to_string
        from django.http import HttpResponse

        return Response({
            'sale': {
                'id': sale.id,
                'created_at': sale.created_at,
                'subtotal': float(sale.subtotal),
                'tax': float(sale.tax),
                'total': float(sale.total),
                'status': sale.status,
                'customer': sale.customer_id_id if sale.customer_id else None,
                'cashier': sale.user_id.first_name if sale.user_id else None,
            },
            'items': [
                {
                    'product': item.product_id.name,
                    'quantity': item.quantity,
                    'unit_price': float(item.unit_price),
                    'total_price': float(item.total_price),
                }
                for item in items
            ],
            'payments': [
                {
                    'method': payment.method,
                    'amount': float(payment.amount),
                    'reference': payment.reference,
                }
                for payment in payments
            ],
        })

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
