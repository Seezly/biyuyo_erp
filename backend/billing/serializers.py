from billing.models import Plan, Subscription, Invoice
from rest_framework import serializers


class PlanSerializer(serializers.ModelSerializer):
    """
    Serializer for the Plan model.
    """

    class Meta:
        model = Plan
        fields = [
            "url",
            "name",
            "price",
            "max_users",
            "max_products",
            "created_at",
            "updated_at",
        ]


class SubscriptionSerializer(serializers.ModelSerializer):
    """
    Serializer for the Subscription model.
    """

    class Meta:
        model = Subscription
        fields = [
            "url",
            "business_id",
            "plan_id",
            "status",
            "start_date",
            "end_date",
        ]


class InvoiceSerializer(serializers.ModelSerializer):
    """
    Serializer for the Invoice model.
    """

    class Meta:
        model = Invoice
        fields = [
            "url",
            "subscription_id",
            "amount",
            "method",
            "status",
            "created_at",
            "updated_at",
        ]
