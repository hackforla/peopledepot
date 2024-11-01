from rest_framework.permissions import BasePermission
from core.api.permission_validation import PermissionValidation
from core.api.user_request import UserRequest
from core.api.profile_request import ProfileRequest

class DenyAny(BasePermission):
    def has_permission(self, __request__, __view__):
        return False

    def has_object_permission(self, __request__, __view__, __obj__):
        return False


class UserMethodPermission(BasePermission):

    def has_permission(self, request, __view__):
        if request.method == "POST":
            UserRequest.validate_fields(request=request)
        return True  # Default to allow the request

    def has_object_permission(self, request, __view__, obj):
        if request.method == "PATCH":
            UserRequest.validate_fields(
                response_related_user=obj, request=request
            )
        return True

class UserProfilePermission(BasePermission):

    def has_permission(self, __request__, __view__):
        return True

    def has_object_permission(self, request, __view__, obj):
        if request.method == "PATCH":
            ProfileRequest.validate_patch_request(request=request)
            return True
