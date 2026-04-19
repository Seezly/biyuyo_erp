from suppliers.models import Supplier, Purchase, PurchaseItem
from rest_framework import serializers


class SupplierSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for the Supplier model.
    """

    class Meta:
        model = Supplier
        fields = "__all__"
        extra_kwargs = {
            "business_id": {"view_name": "business-detail"},
        }


class PurchaseSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for the Purchase model.
    """

    class Meta:
        model = Purchase
        fields = "__all__"
        extra_kwargs = {
            "business_id": {"view_name": "business-detail"},
            "supplier_id": {"view_name": "supplier-detail"},
        }


class PurchaseItemSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for the PurchaseItem model.
    """

    class Meta:
        model = PurchaseItem
        fields = "__all__"
        extra_kwargs = {
            "purchase_id": {"view_name": "purchase-detail"},
            "product_id": {"view_name": "product-detail"},
        }
