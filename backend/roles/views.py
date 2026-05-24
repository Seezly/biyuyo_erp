from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from .models import Role
from .serializers import RoleSerializer, RoleCreateUpdateSerializer


class RoleViewSet(viewsets.ModelViewSet):
    """ViewSet for managing roles"""

    queryset = Role.objects.filter(is_active=True)
    serializer_class = RoleSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["is_active"]
    search_fields = ["name", "description"]
    ordering_fields = ["name", "created_at"]
    ordering = ["name"]

    def get_serializer_class(self):
        """Use different serializers for create/update vs list/retrieve"""
        if self.action in ["create", "update", "partial_update"]:
            return RoleCreateUpdateSerializer
        return RoleSerializer

    def get_queryset(self):
        """Optionally restrict queryset based on query parameters"""
        queryset = Role.objects.all()

        # Filter by active status if specified
        is_active = self.request.query_params.get("is_active")
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == "true")

        return queryset
