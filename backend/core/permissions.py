from rest_framework.permissions import BasePermission


class IsAdminOrBusinessUser(BasePermission):
    """
    Custom permission to allow access only to admin users or business users.
    """

    def has_permission(self, request, view):
        # Check if the user exists andis authenticated
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True  # Allow access to admin users

        # Allow access to business users if the object belongs to their business
        if hasattr(obj, "business"):
            return obj.business == request.user.business

        return False  # Deny access if the object does not have a business attribute

class IsAdminOrBusinessOwner(BasePermission):
    """
    Custom permission to allow access only to businesses owners or admin users.
    """

    def has_permission(self, request):
        return request.user and request.user.groups.first().name == 'owner'
    
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True  # Allow access to admin users

        # Allow access to business users if the object belongs to their business
        if hasattr(obj, "business"):
            return obj.business == request.user.business

        return False  # Deny access if the object does not have a business attribute