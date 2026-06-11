from django.db import models
from inventory.models import Category, Product, InventoryMovement
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import action
from rest_framework.response import Response

from core.mixins import FilteringMixin
from inventory.serializers import (
    CategorySerializer,
    ProductSerializer,
    InventoryMovementSerializer,
)


class CategoryViewSet(FilteringMixin, viewsets.ModelViewSet):
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
        user = self.request.user
        if user.is_superuser:
            qs = super().get_queryset()
            business_id = self.request.query_params.get('business_id')
            if business_id:
                qs = qs.filter(business_id=business_id)
            return self.filter_queryset_with_params(qs)
        queryset = super().get_queryset()
        queryset = queryset.filter(business_id=user.business_id)
        return self.filter_queryset_with_params(queryset)

    def perform_create(self, serializer):
        business_id = self.request.data.get('business_id')
        if self.request.user.is_superuser and business_id:
            serializer.save(business_id=business_id)
        else:
            serializer.save(business_id=self.request.user.business_id)

    def get_object(self):
        obj = super().get_object()
        if self.request.user.is_superuser:
            return obj
        if obj.business_id != self.request.user.business_id:
            raise PermissionDenied("You do not have access to this category.")
        return obj


class ProductViewSet(FilteringMixin, viewsets.ModelViewSet):
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
        user = self.request.user
        if user.is_superuser:
            qs = super().get_queryset()
            business_id = self.request.query_params.get('business_id')
            if business_id:
                qs = qs.filter(business_id=business_id)
            return self.filter_queryset_with_params(qs)
        queryset = super().get_queryset()
        queryset = queryset.filter(business_id=user.business_id)
        return self.filter_queryset_with_params(queryset)

    def perform_create(self, serializer):
        business_id = self.request.data.get('business_id')
        if self.request.user.is_superuser and business_id:
            serializer.save(business_id=business_id)
        else:
            serializer.save(business_id=self.request.user.business_id)

    def get_object(self):
        obj = super().get_object()
        if self.request.user.is_superuser:
            return obj
        if obj.business_id != self.request.user.business_id:
            raise PermissionDenied("You do not have access to this product.")
        return obj

    @action(detail=False, methods=['get'])
    def low_stock(self, request):
        """
        Get products with stock below minimum threshold.
        """
        user = request.user
        products = Product.objects.filter(
            business_id=user.business_id,
            stock__isnull=False,
            min_stock__isnull=False,
            stock__lte=models.F('min_stock'),
        )

        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)


class InventoryMovementViewSet(FilteringMixin, viewsets.ModelViewSet):
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
        user = self.request.user
        if user.is_superuser:
            qs = super().get_queryset()
            business_id = self.request.query_params.get('business_id')
            if business_id:
                qs = qs.filter(business_id=business_id)
            return self.filter_queryset_with_params(qs)
        queryset = super().get_queryset()
        queryset = queryset.filter(business_id=user.business_id)
        return self.filter_queryset_with_params(queryset)

    def perform_create(self, serializer):
        business_id = self.request.data.get('business_id')
        if self.request.user.is_superuser and business_id:
            serializer.save(business_id=business_id)
        else:
            serializer.save(business_id=self.request.user.business_id)

    def get_object(self):
        obj = super().get_object()
        if self.request.user.is_superuser:
            return obj
        if obj.business_id != self.request.user.business_id:
            raise PermissionDenied("You do not have access to this movement.")
        return obj