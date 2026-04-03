from rest_framework_simplejwt.authentication import JWTAuthentication

class CookieJWTAuthentication(JWTAuthentication):
    """
    JWTAuthentication custom class to authenticate users via JWT tokens using cookies

    Return:
        - Return the user and the validated token, else it returns None
    """
    def authenticate(self, request):
        raw_token = request.COOKIES.get("access_token") # Get the JWT access_token

        if raw_token is None:
            return None # If there's no token, then we return None

        validated_token = self.get_validated_token(raw_token) # Validate token
        return self.get_user(validated_token), validated_token # Return the user and the validated token