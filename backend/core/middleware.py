from businesses.models import Business


class BusinessMiddleware:
    """
    Middleware for attaching the business instance to the request based on the user's business association.

    Sets request.business to a Business instance or None.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.business = None

        if request.user.is_authenticated:
            business_id = getattr(request.user, 'business_id_id', None)
            if business_id:
                try:
                    request.business = Business.objects.get(pk=business_id)
                except (Business.DoesNotExist, ValueError):
                    request.business = None

        return self.get_response(request)
