from rest_framework import generics, permissions
from .models import AuditLog
from .serializers import AuditLogSerializer

class AuditLogListView(generics.ListAPIView):
    serializer_class = AuditLogSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['user', 'action', 'model_name', 'object_id']
    search_fields = ['user__email', 'model_name', 'object_repr', 'description']
    ordering_fields = ['timestamp']
    ordering = ['-timestamp']  # Default ordering

    def get_queryset(self):
        # Only allow users to see audit logs for their own business? 
        # For now, we'll allow admins to see all, and regular users to see their own?
        # But the requirement is for audit logging, so let's allow admins to see all.
        # We'll adjust the permission in the URL routing (adminOnly) so only admins can access.
        return AuditLog.objects.all()

class AuditLogDetailView(generics.RetrieveAPIView):
    serializer_class = AuditLogSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = AuditLog.objects.all()