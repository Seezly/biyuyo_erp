from businesses.models import Business


class BusinessMiddleware:
    """
    Middleware for attaching the business to the request based on the user's business association

    Returns:
        request.business: The business associated with the user, or None if not found
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        business_id = (
            request.user.business_id if request.user.is_authenticated else None
        )

        if business_id:
            try:
                request.business = Business.objects.get(id=business_id)
            except Business.DoesNotExist:
                request.business = None
        else:
            request.business = None

        return self.get_response(request)
