from django.contrib.auth.models import Group
from accounts.models import CustomUser
from rest_framework import permissions, viewsets

from core.permissions import IsAdminUser
from accounts.serializers import (
    GroupSerializer,
    UserSerializer,
)


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    Admin-only access with business isolation.
    """

    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return CustomUser.objects.select_related('business_id').order_by("-date_joined")
        return CustomUser.objects.filter(
            business_id=user.business_id
        ).select_related('business_id').order_by("-date_joined")


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    Admin-only access.
    """

    queryset = Group.objects.all().order_by("name")
    serializer_class = GroupSerializer
    permission_classes = [IsAdminUser]
