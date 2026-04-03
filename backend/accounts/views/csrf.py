from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.decorators import api_view
from rest_framework.response import Response

@ensure_csrf_cookie
@api_view(['GET'])
def csrf(request):
    # This method is an API endpoint for setting a CSRF token in cookies in each
    # request. Returns a response.
    return Response({"message": "CSRF cookie set"})