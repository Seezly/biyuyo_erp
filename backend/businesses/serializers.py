from businesses.models import Business
from rest_framework import serializers


class BusinessSerializer(serializers.ModelSerializer):
    """
    Serializer for the Business model.
    """

    class Meta:
        model = Business
        fields = [
            "id",
            "url",
            "name",
            "description",
            "rif",
            "address",
            "state",
            "municipality",
            "phone",
            "email",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]
