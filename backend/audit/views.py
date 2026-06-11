from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from .models import AuditLog
from .serializers import AuditLogSerializer


class AuditLogListView(generics.ListAPIView):
    serializer_class = AuditLogSerializer
    permission_classes = [permissions.IsAdminUser]
    filterset_fields = ['user', 'action', 'model_name', 'object_id']
    search_fields = ['user__email', 'model_name', 'object_repr', 'description']
    ordering_fields = ['timestamp']
    ordering = ['-timestamp']

    def get_queryset(self):
        return AuditLog.objects.select_related('user').filter(
            user__business_id=self.request.business
        )


class AuditLogDetailView(generics.RetrieveAPIView):
    serializer_class = AuditLogSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_object(self):
        obj = generics.get_object_or_404(
            AuditLog.objects.select_related('user'),
            pk=self.kwargs['pk']
        )
        if obj.user is None or obj.user.business_id != self.request.business:
            raise PermissionDenied("You do not have access to this audit log.")
        return obj
