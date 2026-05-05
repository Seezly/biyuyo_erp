from django.db import models
from inventory.models import Category, Product, InventoryMovement
from rest_framework import permissions, viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import action
from rest_framework.response import Response

from inventory.serializers import (
    CategorySerializer,
    ProductSerializer,
    InventoryMovementSerializer,
)


class CategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows categories to be viewed or edited.
    """

    serializer_class = CategorySerializer

    def get_queryset(self):
        user = self.request.user

        return Category.objects.filter(business_id=user.business_id)

    def perform_create(self, serializer):
        serializer.save(business_id=self.request.user.business_id)

    def get_object(self):
        obj = super().get_object()

        if obj.business_id != self.request.user.business_id:
            raise PermissionDenied("You do not have access to this category.")

        return obj


class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows products to be viewed or edited.
    """

    serializer_class = ProductSerializer

    def get_queryset(self):
        user = self.request.user
        return Product.objects.filter(business_id=user.business_id)

    def perform_create(self, serializer):
        serializer.save(business_id=self.request.user.business_id)

    def get_object(self):
        obj = super().get_object()
        if obj.business_id != self.request.user.business_id:
            raise PermissionDenied("No tienes acceso a este producto.")
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
            min_stock__isnull=False
        ).extra(
            where=['stock <= min_stock']
        )

        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)


class InventoryMovementViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows inventory movements to be viewed or edited.
    """

    serializer_class = InventoryMovementSerializer

    def get_queryset(self):
        user = self.request.user
        return InventoryMovement.objects.filter(business_id=user.business_id)

    def perform_create(self, serializer):
        serializer.save(business_id=self.request.user.business_id)

    def get_object(self):
        obj = super().get_object()
        if obj.business_id != self.request.user.business_id:
            raise PermissionDenied("No tienes acceso a este movimiento.")
        return obj
