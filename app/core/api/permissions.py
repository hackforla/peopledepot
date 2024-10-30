from rest_framework.permissions import BasePermission
from core.api.permission_check import PermissionValidation


class DenyAny(BasePermission):
    def has_permission(self, __request__, __view__):
        return False

    def has_object_permission(self, __request__, __view__, __obj__):
        return False


class UserMethodPermission(BasePermission):

    def has_permission(self, request, __view__):
        if request.method == "POST":
            PermissionValidation.validate_user_related_request(request=request)
        return True  # Default to allow the request

    def has_object_permission(self, request, view, obj):
        if request.method == "PATCH":
            PermissionValidation.validate_user_related_request(
                target_user=obj, request=request
            )
        return True


class UserMethodPermission(BasePermission):

    def has_permission(self, request, __view__):
        if request.method == "POST":
            raise 
        return True  # Default to allow the request

    def has_object_permission(self, request, view, obj):
        if request.method == "PATCH":
            PermissionValidation.validate_user_related_request(
                target_user=obj, request=request
            )
        return True
