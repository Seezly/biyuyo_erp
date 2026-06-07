from rest_framework import permissions, viewsets
from rest_framework.exceptions import PermissionDenied

from core.mixins import FilteringMixin
from customers.models import Customer
from customers.serializers import CustomerSerializer


class CustomerViewSet(FilteringMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows customers to be edited or viewed.
    Supports search by name/phone, and ordering.
    """

    queryset = Customer.objects.select_related('business_id').all()
    serializer_class = CustomerSerializer
    search_fields = ['name', 'phone', 'identification_number']
    filter_fields = []
    ordering_fields = ['name', 'created_at']
    default_ordering = ['-created_at']

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(business_id=self.request.user.business_id)
        return self.filter_queryset_with_params(queryset)

    def perform_create(self, serializer):
        serializer.save(business_id=self.request.user.business_id)

    def get_object(self):
        obj = super().get_object()
        if obj.business_id != self.request.user.business_id:
            raise PermissionDenied("You do not have access to this customer.")
        return obj