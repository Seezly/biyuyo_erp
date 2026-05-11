from businesses.models import Business
from rest_framework import permissions, viewsets

from core.mixins import FilteringMixin
from businesses.serializers import BusinessSerializers


class BusinessViewSet(FilteringMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows businesses to be viewed or edited.
    """

    serializer_class = BusinessSerializers
    search_fields = ['name', 'rif', 'email']
    filter_fields = ['state', 'is_active']
    ordering_fields = ['name', 'created_at', 'start_date']
    default_ordering = ['-created_at']

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            queryset = Business.objects.all()
            return self.filter_queryset_with_params(queryset)

        queryset = Business.objects.filter(id=user.business_id)
        return self.filter_queryset_with_params(queryset)
