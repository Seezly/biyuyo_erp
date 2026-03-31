from inventory.models import Category, Product, InventoryMovement
from rest_framework import serializers


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for the Category model.
    """

    class Meta:
        model = Category
        fields = "__all__"


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for the Product model.
    """

    class Meta:
        model = Product
        fields = "__all__"


class InventoryMovementSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for the InventoryMovement model.
    """

    class Meta:
        model = InventoryMovement
        fields = "__all__"
