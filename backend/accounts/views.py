from django.contrib.auth.models import Group
from accounts.models import CustomUser
from rest_framework import permissions, viewsets, views
from rest_framework_simplejwt.views import TokenObtainPairView

from accounts.serializers import (
    GroupSerializer,
    UserSerializer,
    RegisterSerializer,
    CustomTokenSerializer,
)


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = CustomUser.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    queryset = Group.objects.all().order_by("name")
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAdminUser]


class RegisterView(views.APIView):
    """
    API endpoint that allows business owners to register and create a new user
    along with their business.
    """

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        return views.Response(
            {"message": "Business and business owner created successfully."}
        )


class CustomTokenView(TokenObtainPairView):
    """
    API endpoint for user login, which returns a JWT token along with additional
    user information.
    """

    serializer_class = CustomTokenSerializer
    permission_classes = [permissions.AllowAny]
