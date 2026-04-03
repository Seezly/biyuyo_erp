from django.conf import settings
from rest_framework import permissions, views
from accounts.serializers import (
    RegisterSerializer,
    CustomTokenSerializer,
)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


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

class LoginView(views.APIView):
    """
    API endpoint that allows business owners and employees to login and set the
    authorization and refresh tokens into cookies. Returns a response.
    """

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(email=email, password=password)

        if user is None:
            return Response({"error": "Invalid credentials"}, status=401)
        
        # Build tokens using the CustomTokenSerializer to ensure identical claims
        refresh = CustomTokenSerializer.get_token(user)
        access = refresh.access_token

        group = user.groups.first()
        role = group.name if group else None

        response = Response(
            {
                "message": "All good!",
                "user": {
                    "id": user.id,
                    "business_id": user.business_id.id,
                    "business_name": user.business_id.name,
                    "first_name": user.first_name,
                    "role": role,
                },
            }
        )

        secure_flag = not settings.DEBUG

        response.set_cookie(
            key="access_token",
            value=str(access),
            httponly=True,
            secure=secure_flag,
            samesite="lax",
        )

        response.set_cookie(
            key="refresh_token",
            value=str(refresh),
            httponly=True,
            secure=secure_flag,
            samesite="lax",
        )

        return response

class LogoutView(views.APIView):
    """
    API endpoint for users to logout, which sets the JWT token in a blacklist and
    returns a response.
    """

    def post(self, request):

        refresh_token = request.COOKIES.get("refresh_token")

        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
            except Exception:
                pass # Invalid token or already blacklisted

        response = Response({"message": "Logged out!"})

        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")

        return response
