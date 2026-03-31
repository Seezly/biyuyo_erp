from suppliers.models import Supplier, Purchase, PurchaseItem
from rest_framework import serializers


class SupplierSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for the Supplier model.
    """

    class Meta:
        model = Supplier
        fields = "__all__"


class PurchaseSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for the Purchase model.
    """

    class Meta:
        model = Purchase
        fields = "__all__"


class PurchaseItemSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for the PurchaseItem model.
    """

    class Meta:
        model = PurchaseItem
        fields = "__all__"
