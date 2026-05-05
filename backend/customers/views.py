from customers.models import Customer
from rest_framework import permissions, viewsets
from rest_framework.exceptions import PermissionDenied

from customers.serializers import CustomerSerializer


class CustomerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows customers to be edited or viewed
    """

    serializer_class = CustomerSerializer

    def get_queryset(self):
        user = self.request.user
        return Customer.objects.filter(business_id=user.business_id).order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(business_id=self.request.user.business_id)

    def get_object(self):
        obj = super().get_object()
        if obj.business_id != self.request.user.business_id:
            raise PermissionDenied("No tienes acceso a este cliente.")
        return obj
