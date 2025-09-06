from rest_framework import permissions
from users.models import User

class IsVendorOrAdminOrInfluencer(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in [
            User.Role.VENDOR,
            User.Role.SUPER_ADMIN,
            User.Role.INFLUENCER
        ]