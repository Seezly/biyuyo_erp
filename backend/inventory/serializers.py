from inventory.models import Category, Product, InventoryMovement
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for the Category model.
    """

    class Meta:
        model = Category
        fields = "__all__"
        read_only_fields = ["business_id"]


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for the Product model.
    """

    class Meta:
        model = Product
        fields = "__all__"


class InventoryMovementSerializer(serializers.ModelSerializer):
    """
    Serializer for the InventoryMovement model.
    """

    class Meta:
        model = InventoryMovement
        fields = "__all__"
