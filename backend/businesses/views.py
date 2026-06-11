from businesses.models import Business
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied

from core.mixins import FilteringMixin
from businesses.serializers import BusinessSerializer


class BusinessViewSet(FilteringMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows businesses to be viewed or edited.
    """

    serializer_class = BusinessSerializer
    search_fields = ['name', 'rif', 'email']
    filter_fields = ['state', 'is_active']
    ordering_fields = ['name', 'created_at']
    default_ordering = ['-created_at']

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            queryset = Business.objects.all()
            return self.filter_queryset_with_params(queryset)

        queryset = Business.objects.filter(id=user.business_id)
        return self.filter_queryset_with_params(queryset)

    def get_object(self):
        obj = super().get_object()
        user = self.request.user

        if user.is_superuser:
            return obj

        if obj.id != user.business_id_id:
            raise PermissionDenied("You do not have access to this business.")

        return obj
