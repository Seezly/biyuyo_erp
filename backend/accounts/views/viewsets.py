from django.contrib.auth.models import Group
from accounts.models import CustomUser, ReminderSettings
from rest_framework import permissions, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from core.permissions import IsAdminOrBusinessUser, IsAdminUser
from accounts.serializers import (
    GroupSerializer,
    ReminderSettingsSerializer,
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

    @action(detail=False, methods=['post'], url_path='change-password')
    def change_password(self, request):
        user = request.user
        current_password = request.data.get('current_password')
        new_password = request.data.get('new_password')

        if not current_password or not new_password:
            return Response(
                {'detail': 'Se requieren current_password y new_password'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not user.check_password(current_password):
            return Response(
                {'detail': 'La contraseña actual es incorrecta'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user.set_password(new_password)
        user.save()

        return Response({'detail': 'Contraseña cambiada correctamente'})


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    Admin-only access.
    """

    queryset = Group.objects.all().order_by("name")
    serializer_class = GroupSerializer
    permission_classes = [IsAdminUser]


class ReminderSettingsViewSet(viewsets.ModelViewSet):
    serializer_class = ReminderSettingsSerializer
    permission_classes = [IsAdminOrBusinessUser]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return ReminderSettings.objects.all()
        return ReminderSettings.objects.filter(business_id=user.business_id)

    def perform_create(self, serializer):
        serializer.save(business_id=self.request.user.business_id)

    @action(detail=False, methods=["get", "patch"], url_path="current")
    def current(self, request):
        settings, _ = ReminderSettings.objects.get_or_create(
            business_id=request.user.business_id
        )
        if request.method == "PATCH":
            serializer = self.get_serializer(settings, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        return Response(self.get_serializer(settings).data)
