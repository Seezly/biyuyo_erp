from businesses.models import Business
from accounts.authentication import CookieJWTAuthentication


class BusinessMiddleware:
    """
    Middleware for attaching the business instance to the request based on the user's business association.

    Supports impersonation via X-Business-Id header for admin/superadmin users.
    Sets request.business to a Business instance or None.
    Sets request.impersonated to True/False.

    Authenticates via JWT cookie when Django session auth doesn't set request.user.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.business = None
        request.impersonated = False

        if not request.user.is_authenticated:
            auth = CookieJWTAuthentication()
            result = auth.authenticate(request)
            if result:
                request.user, request.auth = result

        if request.user.is_authenticated:
            impersonate_id = request.META.get("HTTP_X_BUSINESS_ID")
            if impersonate_id and (
                request.user.is_superuser
                or request.user.groups.filter(name="admin").exists()
            ):
                try:
                    request.business = Business.objects.get(pk=impersonate_id)
                    request.impersonated = True
                    return self.get_response(request)
                except (Business.DoesNotExist, ValueError):
                    pass

            business_id = getattr(request.user, "business_id_id", None)
            if business_id:
                try:
                    request.business = Business.objects.get(pk=business_id)
                except (Business.DoesNotExist, ValueError):
                    request.business = None

        return self.get_response(request)
