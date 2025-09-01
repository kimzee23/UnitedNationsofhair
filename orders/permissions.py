
from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user and request.user.is_staff:
            return True
        # Order has .user
        return getattr(obj, "user_id", None) == getattr(request.user, "id", None)

    def has_permission(self, request, view):
        # Authenticated users only by default
        return request.user and request.user.is_authenticated
