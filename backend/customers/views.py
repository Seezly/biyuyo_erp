from rest_framework import permissions, viewsets
from rest_framework.exceptions import PermissionDenied

from core.mixins import BusinessFilterMixin, FilteringMixin
from customers.models import Customer
from customers.serializers import CustomerSerializer


class CustomerViewSet(BusinessFilterMixin, FilteringMixin, viewsets.ModelViewSet):
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
        business = self.get_business_filter()
        if business:
            queryset = queryset.filter(business_id=business)
        return self.filter_queryset_with_params(queryset)

    def perform_create(self, serializer):
        serializer.save(business_id=self.request.business)

    def get_object(self):
        obj = super().get_object()
        business = self.get_business_filter()
        if business and obj.business_id != business:
            raise PermissionDenied("You do not have access to this customer.")
        return obj
