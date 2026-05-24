from rest_framework import serializers
from .models import Role


class RoleSerializer(serializers.ModelSerializer):
    """Serializer for Role model"""
    permission_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Role
        fields = ['id', 'name', 'description', 'permission_count', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_permission_count(self, obj):
        return obj.permissions.count()


class RoleCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating and updating Role instances"""
    permissions = serializers.PrimaryKeyRelatedField(
        queryset=Role._meta.get_field('permissions').related_model.objects.all(),
        many=True,
        required=False
    )
    
    class Meta:
        model = Role
        fields = ['name', 'description', 'permissions', 'is_active']
    
    def validate_name(self, value):
        """Ensure role name is unique"""
        queryset = Role.objects.all()
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)
        if queryset.filter(name__iexact=value).exists():
            raise serializers.ValidationError("A role with this name already exists.")
        return value