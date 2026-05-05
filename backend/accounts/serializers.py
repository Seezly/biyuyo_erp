from django.contrib.auth.models import Group
from accounts.models import CustomUser
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from businesses.models import Business
from accounts.services.user_service import create_user_with_role


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.
    """

    # role = serializers.SerializerMethodField()

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
            "created_at",
            "updated_at",
        ]
        extra_kwargs = {"url": {"view_name": "user-detail"}}

    def get_role(self, obj):
        group = obj.groups.first()
        return group.name if group else None


class GroupSerializer(serializers.ModelSerializer):
    """
    Serializer for the Group model.
    """

    class Meta:
        model = Group
        fields = ["url", "name"]


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for business owner registration, along with the necessary fields
    for creating a new user.
    """

    business_name = serializers.CharField(max_length=255, required=True)
    business_description = serializers.CharField(required=True)
    business_rif = serializers.CharField(max_length=10, required=True)
    business_address = serializers.CharField(max_length=255, required=True)
    business_state = serializers.CharField(max_length=255, required=True)
    business_municipality = serializers.CharField(max_length=255, required=True)

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
            "business_state",
            "business_municipality",
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
        business_state = validated_data.pop("business_state")
        business_municipality = validated_data.pop("business_municipality")

        business = Business.objects.create(
            name=business_name,
            description=business_description,
            rif=business_rif,
            address=business_address,
            state=business_state,
            municipality=business_municipality,
            phone=validated_data["phone"],
            email=validated_data["email"],
        )

        user = create_user_with_role(validated_data, business, "owner")

        user.save()

        return user


class CustomTokenSerializer(TokenObtainPairSerializer):
    """
    Serializer for user login, which extends the TokenObtainPairSerializer to
    include additional user information in the token response.
    """

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # extra info from user
        token["business_id"] = user.business_id.id
        token["business_name"] = user.business_id.name
        token["first_name"] = user.first_name
        # Use first Group name as the role
        group = user.groups.first()
        token["role"] = group.name if group else None

        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        group = self.user.groups.first()
        data["user"] = {
            "id": self.user.id,
            "business_id": self.user.business_id.id,
            "business_name": self.user.business_id.name,
            "first_name": self.user.first_name,
            "role": group.name if group else None,
        }

        return data
