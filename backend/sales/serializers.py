from sales.models import Sale, SaleItem, Payment
from rest_framework import serializers


class SaleSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for the Sale model.
    """

    class Meta:
        model = Sale
        fields = "__all__"
        extra_kwargs = {
            "user_id": {"view_name": "user-detail"},
        }


class SaleItemSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for the SaleItem model.
    """

    class Meta:
        model = SaleItem
        fields = "__all__"


class PaymentSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for the Payment model.
    """

    class Meta:
        model = Payment
        fields = "__all__"
