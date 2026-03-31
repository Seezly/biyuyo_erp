from customers.models import Customer
from rest_framework import serializers


class CustomerSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for the Customer model.
    """

    class Meta:
        model = Customer
        fields = [
            "url",
            "name",
            "business_id",
            "phone",
            "identification_number",
            "created_at",
            "updated_at",
        ]
