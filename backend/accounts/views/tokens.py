from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import views, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from accounts.serializers import CustomTokenSerializer


class RefreshView(views.APIView):
    """
    API endpoint for JWT token refresh. Returns a response
    """
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def post(self, request):
        refresh_token = request.COOKIES.get("refresh_token")

        if not refresh_token:
            return Response({"error": "No refresh token"}, status=401)
        try:
            old_refresh = RefreshToken(refresh_token)   

            # Get the user from the token's user_id claim
            user_id = old_refresh.get("user_id")
            User = get_user_model()
            try:
                user = User.objects.get(pk=user_id)
            except User.DoesNotExist:
                return Response({"error": "Invalid token (user not found)"}, status=401)

            rotate = settings.SIMPLE_JWT.get("ROTATE_REFRESH_TOKENS", False)
            blacklist = settings.SIMPLE_JWT.get("BLACKLIST_AFTER_ROTATION", False)

            if rotate:
                # create new refresh for the user
                new_refresh = RefreshToken.for_user(user)
                # blacklist the old refresh if configured
                if blacklist:
                    try:
                        old_refresh.blacklist()
                    except Exception:
                        pass

                access = new_refresh.access_token
                resp_refresh = new_refresh
            else:
                access = old_refresh.access_token
                resp_refresh = old_refresh

            response = Response({"message": "Refreshed"})

            secure_flag = not settings.DEBUG

            response.set_cookie(
                key="access_token",
                value=str(access),
                httponly=True,
                secure=secure_flag,
                samesite="lax",
            )

            # If we rotated, update the refresh cookie too
            if rotate:
                response.set_cookie(
                    key="refresh_token",
                    value=str(resp_refresh),
                    httponly=True,
                    secure=secure_flag,
                    samesite="lax",
                )

            return response

        except Exception:
            return Response({"error": "Invalid refresh token"}, status=401)


class CustomTokenView(TokenObtainPairView):
    """
    API endpoint for obtaining JWT tokens with extra user info.
    """

    serializer_class = CustomTokenSerializer
    permission_classes = [permissions.AllowAny]