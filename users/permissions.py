from rest_framework import permissions
from users.models import User


class RolePermission(permissions.BasePermission):
    allowed_roles = []

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role in self.allowed_roles
        )

    @classmethod
    def for_roles(cls, *roles):
        return type(
            f"RolePermission_{'_'.join(roles)}",
            (cls,),
            {"allowed_roles": roles},
        )

IsAdmin = RolePermission.for_roles(User.Role.SUPER_ADMIN)
IsVendorOrAdmin = RolePermission.for_roles(User.Role.VENDOR, User.Role.SUPER_ADMIN)
IsInfluencerOrAdmin = RolePermission.for_roles(User.Role.INFLUENCER, User.Role.SUPER_ADMIN)
