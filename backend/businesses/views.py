from businesses.models import Business
from rest_framework import permissions, viewsets

from businesses.serializers import BusinessSerializers


class BusinessViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows businesses to be viewed or edited.
    """

    serializer_class = BusinessSerializers

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return Business.objects.all().order_by("-created_at")

        return Business.objects.filter(
            id=user.business_id
        ).order_by("-start_date")
