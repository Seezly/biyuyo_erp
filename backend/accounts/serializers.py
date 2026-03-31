from django.contrib.auth.models import Group
from accounts.models import CustomUser
from rest_framework import serializers

from businesses.models import Business


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


class RegisterSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for business owner registration, along with the necessary fields
    for creating a new user.
    """

    business_name = serializers.CharField(max_length=255, required=True)
    business_description = serializers.CharField(required=True)
    business_rif = serializers.CharField(max_length=10, required=True)
    business_address = serializers.CharField(max_length=255, required=True)

    class Meta:
        """
        Meta class to define the fields that the RegisterSerializer needs and
        the behavior of each field
        """

        model = CustomUser
        fields = [
            "email",
            "first_name",
            "last_name",
            "identification_number",
            "phone",
            "password",
            "is_active",
            "is_staff",
            "business_name",
            "business_description",
            "business_rif",
            "business_address",
        ]

        extra_kwargs = {
            "password": {"write_only": True},
            "is_active": {"read_only": True},
            "is_staff": {"read_only": True},
        }

    def create(self, validated_data):
        business_name = validated_data.pop("business_name")
        business_description = validated_data.pop("business_description")
        business_rif = validated_data.pop("business_rif")
        business_address = validated_data.pop("business_address")

        business = Business.objects.create(
            name=business_name,
            description=business_description,
            rif=business_rif,
            address=business_address,
        )

        user = CustomUser.objects.create_user(
            **validated_data, role="owner", business_id=business
        )

        return user
