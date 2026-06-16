from django.contrib.auth.models import Group
from accounts.models import CustomUser, ReminderSettings
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from core.permissions import IsAdminUser, IsAdminOrBusinessUser
from core.mixins import BusinessFilterMixin
from accounts.serializers import (
    GroupSerializer,
    ReminderSettingsSerializer,
    UserSerializer,
)


class UserViewSet(BusinessFilterMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    Admin-only access with business isolation.
    """

    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        business = self.get_business_filter()
        if business:
            return CustomUser.objects.filter(
                business_id=business
            ).select_related('business_id').order_by("-date_joined")
        return CustomUser.objects.select_related('business_id').order_by("-date_joined")

    def create(self, request, *args, **kwargs):
        role_name = request.data.get('role')
        response = super().create(request, *args, **kwargs)
        if response.status_code == 201 and role_name:
            user = CustomUser.objects.get(pk=response.data['id'])
            try:
                group = Group.objects.get(name=role_name)
                user.groups.add(group)
            except Group.DoesNotExist:
                pass
        return response

    def update(self, request, *args, **kwargs):
        role_name = request.data.get('role')
        response = super().update(request, *args, **kwargs)
        if response.status_code == 200 and role_name:
            user = self.get_object()
            user.groups.clear()
            try:
                group = Group.objects.get(name=role_name)
                user.groups.add(group)
            except Group.DoesNotExist:
                pass
        return response

    def perform_create(self, serializer):
        serializer.save(business_id=self.request.business)

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


class ReminderSettingsViewSet(BusinessFilterMixin, viewsets.ModelViewSet):
    serializer_class = ReminderSettingsSerializer
    permission_classes = [IsAdminOrBusinessUser]

    def get_queryset(self):
        business = self.get_business_filter()
        if business:
            return ReminderSettings.objects.filter(business_id=business)
        return ReminderSettings.objects.all()

    def perform_create(self, serializer):
        serializer.save(business_id=self.request.business)

    @action(detail=False, methods=["get", "patch"], url_path="current")
    def current(self, request):
        settings, _ = ReminderSettings.objects.get_or_create(
            business_id=request.business
        )
        if request.method == "PATCH":
            serializer = self.get_serializer(settings, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        return Response(self.get_serializer(settings).data)
