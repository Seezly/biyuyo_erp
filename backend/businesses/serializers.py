from businesses.models import Business
from rest_framework import serializers


class BusinessSerializers(serializers.HyperlinkedModelSerializer):
    """
    Serializer for the Business model.
    """

    class Meta:
        model = Business
        fields = [
            "url",
            "name",
            "description",
            "rif",
            "address",
            "phone",
            "email",
            "is_active",
            "created_at",
            "updated_at",
        ]
