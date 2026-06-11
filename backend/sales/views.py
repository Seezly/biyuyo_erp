from django.db import transaction, models
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework import status

from core.mixins import FilteringMixin
from sales.models import Sale, SaleItem, Payment
from sales.serializers import SaleSerializer, SaleItemSerializer, PaymentSerializer
from inventory.models import Product


class SaleViewSet(FilteringMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows sales to be viewed or edited.
    Includes stock validation and automatic stock deduction.
    Supports search by sale ID or customer name, filtering by status, and ordering.
    """

    queryset = Sale.objects.select_related('customer_id', 'user_id').all()
    serializer_class = SaleSerializer
    search_fields = ['id', 'customer_id__name']
    filter_fields = ['status']
    ordering_fields = ['created_at', 'total', 'subtotal']
    default_ordering = ['-created_at']

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(business_id=self.request.user.business_id).prefetch_related('saleitem_set', 'payment_set')
        return self.filter_queryset_with_params(queryset)

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
        items = sale.saleitem_set.select_related('product_id').all()
        payments = sale.payment_set.all()

        return Response({
            'sale': {
                'id': sale.id,
                'created_at': sale.created_at,
                'subtotal': float(sale.subtotal),
                'tax': float(sale.tax),
                'total': float(sale.total),
                'status': sale.status,
                'customer': sale.customer_id.id if sale.customer_id else None,
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

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        data = request.data
        items_data = data.get('items', [])

        errors = []
        for item in items_data:
            product_id = item.get('product')
            quantity = item.get('quantity', 0)

            if product_id and quantity > 0:
                try:
                    product = Product.objects.select_for_update().get(
                        id=product_id, business_id=request.user.business_id
                    )
                    if product.stock is not None and product.stock < quantity:
                        errors.append(
                            f"Stock insuficiente para '{product.name}'. "
                            f"Disponible: {product.stock}, solicitado: {quantity}"
                        )
                except Product.DoesNotExist:
                    errors.append(f"Producto con ID {product_id} no encontrado")

        if errors:
            return Response({'errors': errors}, status=status.HTTP_400_BAD_REQUEST)

        return super().create(request, *args, **kwargs)

    @transaction.atomic
    def perform_create(self, serializer):
        request = self.request
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
                    product = Product.objects.select_for_update().get(
                        id=product_id, business_id=request.user.business_id
                    )

                    SaleItem.objects.create(
                        sale_id=sale,
                        product_id=product,
                        quantity=quantity,
                        unit_price=item_data.get('unit_price', float(product.sell_price)),
                        total_price=item_data.get('total_price', float(product.sell_price) * quantity)
                    )

                    if product.stock is not None:
                        Product.objects.filter(pk=product.pk).update(
                            stock=models.F('stock') - quantity
                        )
                except Product.DoesNotExist:
                    pass

    def get_object(self):
        obj = super().get_object()
        if obj.business_id != self.request.user.business_id:
            raise PermissionDenied("You do not have access to this sale.")
        return obj


class SaleItemViewSet(FilteringMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows sale items to be viewed or edited.
    """

    queryset = SaleItem.objects.select_related('sale_id', 'product_id').all()
    serializer_class = SaleItemSerializer
    search_fields = ['product_id__name']
    filter_fields = ['sale_id', 'product_id']
    ordering_fields = ['created_at', 'quantity']
    default_ordering = ['-created_at']

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(sale_id__business_id=self.request.user.business_id)
        return self.filter_queryset_with_params(queryset)

    def perform_create(self, serializer):
        sale = serializer.validated_data.get('sale_id')
        if sale and sale.business_id != self.request.user.business_id:
            raise PermissionDenied("No tienes acceso a esta venta.")
        serializer.save()

    def get_object(self):
        obj = super().get_object()
        if obj.sale_id.business_id != self.request.user.business_id:
            raise PermissionDenied("You do not have access to this item.")
        return obj


class PaymentViewSet(FilteringMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows payments to be viewed or edited.
    Supports search by reference, filtering by method/status, and ordering.
    """

    queryset = Payment.objects.select_related('sale_id').all()
    serializer_class = PaymentSerializer
    search_fields = ['reference']
    filter_fields = ['method', 'status']
    ordering_fields = ['created_at', 'amount']
    default_ordering = ['-created_at']

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(sale_id__business_id=self.request.user.business_id)
        return self.filter_queryset_with_params(queryset)

    def perform_create(self, serializer):
        sale = serializer.validated_data.get('sale_id')
        if sale and sale.business_id != self.request.user.business_id:
            raise PermissionDenied("No tienes acceso a esta venta.")
        serializer.save()

    def get_object(self):
        obj = super().get_object()
        if obj.sale_id.business_id != self.request.user.business_id:
            raise PermissionDenied("You do not have access to this payment.")
        return obj