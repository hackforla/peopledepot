from rest_framework.permissions import BasePermission
from core.api.permission_check import FieldPermissionCheck

class DenyAny(BasePermission):
    def has_permission(self, __request__, __view__):
        return False

    def has_object_permission(self, __request__, __view__, __obj__):
        return False


class UserMethodPermission(BasePermission):

    def has_permission(self, request, __view__):
        if request.method == "POST":
            FieldPermissionCheck.validate_user_related_request(request=request)
        return True  # Default to allow the request

    def has_object_permission(self, request, view, obj):
        if request.method == "PATCH":
            FieldPermissionCheck.validate_user_related_request(
                target_user=obj, request=request
            )
        return True
