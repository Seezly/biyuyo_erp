from suppliers.models import Supplier, Purchase, PurchaseItem
from rest_framework import serializers


class SupplierSerializer(serializers.ModelSerializer):
    """
    Serializer for the Supplier model.
    """

    class Meta:
        model = Supplier
        fields = "__all__"
        read_only_fields = ["business_id", "created_at", "updated_at"]


class PurchaseSerializer(serializers.ModelSerializer):
    """
    Serializer for the Purchase model.
    """

    class Meta:
        model = Purchase
        fields = "__all__"
        read_only_fields = ["business_id", "created_at", "updated_at"]


class PurchaseItemSerializer(serializers.ModelSerializer):
    """
    Serializer for the PurchaseItem model.
    """

    class Meta:
        model = PurchaseItem
        fields = "__all__"
        read_only_fields = ["created_at", "updated_at"]
