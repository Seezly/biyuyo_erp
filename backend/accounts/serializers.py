from django.contrib.auth.models import Group
from accounts.models import CustomUser
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for the User model.
    """

    class Meta:
        model = CustomUser
        fields = [
            "url",
            "email",
            "business_id",
            "first_name",
            "last_name",
            "groups",
            "identification_number",
            "phone",
            "is_active",
            "role",
            "created_at",
            "updated_at",
        ]


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for the Group model.
    """

    class Meta:
        model = Group
        fields = ["url", "name"]
