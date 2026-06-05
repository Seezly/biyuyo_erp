from customers.models import Customer
from rest_framework import serializers


class CustomerSerializer(serializers.ModelSerializer):
    """
    Serializer for the Customer model.
    """

    class Meta:
        model = Customer
        fields = [
            "id",
            "name",
            "phone",
            "identification_number",
            "business_id",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "business_id", "created_at", "updated_at"]
