from sales.models import Sale, SaleItem, Payment
from rest_framework import serializers


class SaleSerializer(serializers.ModelSerializer):
    """
    Serializer for the Sale model.
    """

    class Meta:
        model = Sale
        fields = "__all__"


class SaleItemSerializer(serializers.ModelSerializer):
    """
    Serializer for the SaleItem model.
    """

    class Meta:
        model = SaleItem
        fields = "__all__"


class PaymentSerializer(serializers.ModelSerializer):
    """
    Serializer for the Payment model.
    """

    class Meta:
        model = Payment
        fields = "__all__"
