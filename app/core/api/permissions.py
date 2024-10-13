from rest_framework.permissions import BasePermission
from core.api.permission_check import PermissionCheck

class DenyAny(BasePermission):
    def has_permission(self, __request__, __view__):
        return False

    def has_object_permission(self, __request__, __view__, __obj__):
        return False


class CheckUserPermission:
    @staticmethod
    def validate_post(request):
        if "time_zone" not in request.data:
            request.data["time_zone"] = "America/Los_Angeles"
        PermissionCheck.validate_user_fields_postable(request.user, request.data)

    @staticmethod
    def validate_patch(request, obj):
        PermissionCheck.validate_user_fields_patchable(request.user, obj, request.data)


class UserPermissionCheck(BasePermission):

    def has_permission(self, request, __view__):
        if request.method == "POST":
            CheckUserPermission.validate_post(request)
        return True  # Default to allow the request

    def has_object_permission(self, request, view, obj):
        if request.method == "PATCH":
            PermissionCheck.validate_user_fields_patchable(
                request.user, obj, request.data
            )
        return True
