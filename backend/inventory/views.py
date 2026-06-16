from django.db import models
from inventory.models import Category, Product, InventoryMovement
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import action
from rest_framework.response import Response

from core.mixins import BusinessFilterMixin, FilteringMixin
from inventory.serializers import (
    CategorySerializer,
    ProductSerializer,
    InventoryMovementSerializer,
)


class CategoryViewSet(BusinessFilterMixin, FilteringMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows categories to be viewed or edited.
    Supports search, filtering, and ordering.
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    search_fields = ['name']
    filter_fields = []
    ordering_fields = ['name', 'created_at']
    default_ordering = ['-created_at']

    def get_queryset(self):
        queryset = super().get_queryset()
        business = self.get_business_filter()
        if business:
            queryset = queryset.filter(business_id=business)
        return self.filter_queryset_with_params(queryset)

    def perform_create(self, serializer):
        serializer.save(business_id=self.get_required_business())

    def get_object(self):
        obj = super().get_object()
        business = self.get_business_filter()
        if business and obj.business_id != business:
            raise PermissionDenied("You do not have access to this category.")
        return obj


class ProductViewSet(BusinessFilterMixin, FilteringMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows products to be viewed or edited.
    Supports search by name/sku, filtering by category, and ordering.
    """

    queryset = Product.objects.select_related('category_id').all()
    serializer_class = ProductSerializer
    search_fields = ['name', 'sku', 'description']
    filter_fields = ['category_id', 'stock']
    ordering_fields = ['created_at', 'name', 'stock', 'sell_price', 'cost_price']
    default_ordering = ['-created_at']

    def get_queryset(self):
        queryset = super().get_queryset()
        business = self.get_business_filter()
        if business:
            queryset = queryset.filter(business_id=business)
        return self.filter_queryset_with_params(queryset)

    def perform_create(self, serializer):
        serializer.save(business_id=self.get_required_business())

    def get_object(self):
        obj = super().get_object()
        business = self.get_business_filter()
        if business and obj.business_id != business:
            raise PermissionDenied("You do not have access to this product.")
        return obj

    @action(detail=False, methods=['get'])
    def low_stock(self, request):
        """
        Get products with stock below minimum threshold.
        """
        products = Product.objects.filter(
            business_id=self.get_required_business(),
            stock__isnull=False,
            min_stock__isnull=False,
            stock__lte=models.F('min_stock'),
        )

        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)


class InventoryMovementViewSet(BusinessFilterMixin, FilteringMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows inventory movements to be viewed or edited.
    Supports filtering by type and ordering.
    """

    queryset = InventoryMovement.objects.select_related('product_id').all()
    serializer_class = InventoryMovementSerializer
    search_fields = ['reference']
    filter_fields = ['type', 'product_id']
    ordering_fields = ['created_at', 'type', 'quantity']
    default_ordering = ['-created_at']

    def get_queryset(self):
        queryset = super().get_queryset()
        business = self.get_business_filter()
        if business:
            queryset = queryset.filter(business_id=business)
        return self.filter_queryset_with_params(queryset)

    def perform_create(self, serializer):
        serializer.save(business_id=self.get_required_business())

    def get_object(self):
        obj = super().get_object()
        business = self.get_business_filter()
        if business and obj.business_id != business:
            raise PermissionDenied("You do not have access to this movement.")
        return obj
