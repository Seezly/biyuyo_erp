from rest_framework.permissions import BasePermission


class IsAdminOrBusinessUser(BasePermission):
    """
    Default permission: allows access to any authenticated user.
    Object-level permission checks that the object belongs to the user's business.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        user_business_id = getattr(request.user, 'business_id_id', None)
        if user_business_id is None:
            return False

        obj_business_id = getattr(obj, 'business_id_id', None)
        if obj_business_id is None:
            obj_business_id = getattr(obj, 'business_id', None)

        return obj_business_id == user_business_id


class IsAdminOrBusinessOwner(BasePermission):
    """
    Allows access to admin users or business owners (users in the 'owner' group).
    """

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True
        return request.user.groups.filter(name='owner').exists()

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        user_business_id = getattr(request.user, 'business_id_id', None)
        if user_business_id is None:
            return False

        obj_business_id = getattr(obj, 'business_id_id', None)
        if obj_business_id is None:
            obj_business_id = getattr(obj, 'business_id', None)

        return obj_business_id == user_business_id


class IsBusinessAdmin(BasePermission):
    """
    Allows access only to users who are in the 'admin' or 'owner' group
    for their business, or superusers.
    """

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True
        return request.user.groups.filter(name__in=['admin', 'owner']).exists()


class IsAdminUser(BasePermission):
    """
    Allows access only to admin users (superusers or staff).
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_staff
