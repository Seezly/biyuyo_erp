from inventory.models import Category, Product, InventoryMovement
from rest_framework import permissions, viewsets

from inventory.serializers import (
    CategorySerializer,
    ProductSerializer,
    InventoryMovementSerializer,
)


class CategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows categories to be viewed or edited.
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows products to be viewed or edited.
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class InventoryMovementViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows inventory movements to be viewed or edited.
    """

    queryset = InventoryMovement.objects.all()
    serializer_class = InventoryMovementSerializer
