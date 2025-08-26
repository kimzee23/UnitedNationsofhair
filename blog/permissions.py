from rest_framework import permissions

from users.models import User


class IsInfluencerOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (
            request.user.is_authenticated and
            request.user.role in [User.Role.INFLUENCER, User.Role.SUPER_ADMIN]
        )