from rest_framework import permissions

class IsSuperOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow supersuer to add and edit objects.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            if request.user.profile:
                return True
            else:
                return False
            
        # Write permissions are only allowed to the owner of the snippet.
        if request.user.is_superuser:
            return True
        else:
            return False


class IsSuperOrProfileOwner(permissions.BasePermission):
    """
    Custom permission to only allow superusers or owners of an object to see and edit it.
    """

    def has_object_permission(self, request, view, obj):
        # this is for any request method
            if request.user.profile == obj or request.user.is_superuser:
                return True
            return False

    def has_permission(self, request, view):
        return bool(
            request.user.is_authenticated and
            (request.user.is_superuser or request.user.profile)
        )