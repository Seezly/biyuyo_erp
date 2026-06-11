from billing.models import Plan, Subscription, Invoice
from rest_framework import serializers


class PlanSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for the Plan model.
    """

    class Meta:
        model = Plan
        fields = [
            "id",
            "url",
            "name",
            "price",
            "max_users",
            "max_products",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]
        extra_kwargs = {"url": {"view_name": "plans-detail"}}


class SubscriptionSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for the Subscription model.
    """

    class Meta:
        model = Subscription
        fields = [
            "id",
            "url",
            "business_id",
            "plan_id",
            "status",
            "start_date",
            "end_date",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["business_id", "created_at", "updated_at"]
        extra_kwargs = {"url": {"view_name": "subscriptions-detail"}}


class InvoiceSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for the Invoice model.
    """

    class Meta:
        model = Invoice
        fields = [
            "id",
            "url",
            "subscription_id",
            "amount",
            "method",
            "status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]
        extra_kwargs = {"url": {"view_name": "invoices-detail"}}
