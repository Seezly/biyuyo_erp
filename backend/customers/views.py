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
        user = self.request.user
        if user.is_superuser:
            qs = super().get_queryset()
            business_id = self.request.query_params.get('business_id')
            if business_id:
                qs = qs.filter(business_id=business_id)
            return self.filter_queryset_with_params(qs)
        queryset = super().get_queryset()
        queryset = queryset.filter(business_id=user.business_id)
        return self.filter_queryset_with_params(queryset)

    def perform_create(self, serializer):
        business_id = self.request.data.get('business_id')
        if self.request.user.is_superuser and business_id:
            serializer.save(business_id=business_id)
        else:
            serializer.save(business_id=self.request.user.business_id)

    def get_object(self):
        obj = super().get_object()
        if self.request.user.is_superuser:
            return obj
        if obj.business_id != self.request.user.business_id:
            raise PermissionDenied("You do not have access to this customer.")
        return obj