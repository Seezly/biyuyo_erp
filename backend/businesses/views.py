from businesses.models import Business
from rest_framework import permissions, viewsets

from businesses.serializers import BusinessSerializers


class BusinessViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows businesses to be viewed or edited.
    """

    queryset = Business.objects.all()
    serializer_class = BusinessSerializers
