from rest_framework.permissions import BasePermission

from .validate_request import validate_post_fields, validate_patch_fields


class HasUserPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST":
            validate_post_fields(request=request, view=view)
        return True  # Default to allow the request

    def has_object_permission(self, request, view, obj):
        if request.method == "PATCH":
            validate_patch_fields(
                obj=obj, request=request
            )
        return True
