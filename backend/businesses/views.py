from businesses.models import Business
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied

from core.mixins import BusinessFilterMixin, FilteringMixin
from businesses.serializers import BusinessSerializer


class BusinessViewSet(BusinessFilterMixin, FilteringMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows businesses to be viewed or edited.
    Superadmins can see all businesses. Admins see all when not impersonating.
    """

    serializer_class = BusinessSerializer
    search_fields = ['name', 'rif', 'email']
    filter_fields = ['state', 'is_active']
    ordering_fields = ['name', 'created_at']
    default_ordering = ['-created_at']

    def get_queryset(self):
        business = self.get_business_filter()
        if business:
            queryset = Business.objects.filter(id=business.id)
        else:
            queryset = Business.objects.all()
        return self.filter_queryset_with_params(queryset)

    def get_object(self):
        obj = super().get_object()
        business = self.get_business_filter()
        if business and obj.id != business.id:
            raise PermissionDenied("You do not have access to this business.")
        return obj
