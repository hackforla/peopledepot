from rest_framework.permissions import BasePermission

from core.api.generic_request import GenericRequest


class DenyAny(BasePermission):
    def has_permission(self, __request__, __view__):
        return False

    def has_object_permission(self, __request__, __view__, __obj__):
        return False

class GenericPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST":
            GenericRequest.validate_post_fields(request=request, view=view)
        return True  # Default to allow the request

    def has_object_permission(self, request, view, obj):
        if request.method == "PATCH":
            GenericRequest.validate_patch_fields(
                view=view, obj=obj, request=request
            )
        return True
