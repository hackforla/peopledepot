from rest_framework.permissions import SAFE_METHODS
from rest_framework.permissions import BasePermission

from core.permission_util import PermissionUtil
from core.user_cru_permissions import UserCruPermissions


class IsAdmin(BasePermission):
    def has_permission(self, request, __view__):
        return PermissionUtil.is_admin(request.user)

    def has_object_permission(self, request, __view__, __obj__):
        return PermissionUtil.is_admin(request.user)


class IsAdminOrReadOnly(BasePermission):
    """
    Custom permission to only allow admins to edit it, while allowing read-only access to authenticated users.
    """

    def has_permission(self, request, view):
        # Allow any read-only actions if the user is authenticated
        if request.method in SAFE_METHODS:
            return request.user and request.user.is_authenticated

        # Allow edit actions (POST, PUT, DELETE) only if the user is an admin
        return PermissionUtil.is_admin(request.user)


class UserPermissions(BasePermission):
    # User view restricts read access to users
    def has_permission(self, __request__, __view__):
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return (
                PermissionUtil.get_lowest_ranked_permission_type(request.user, obj)
                != ""
            )
        highest_ranked_name = PermissionUtil.get_lowest_ranked_permission_type(
            request.user, obj
        )
        read_fields = UserCruPermissions.read_fields[highest_ranked_name]
        return len(set(read_fields)) > 0


class DenyAny(BasePermission):
    def has_permission(self, __request__, __view__):
        return False

    def has_object_permission(self, __request__, __view__, __obj__):
        return False
