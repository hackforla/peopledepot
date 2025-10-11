from rest_framework.permissions import BasePermission

from .validate_request import validate_post_fields, validate_patch_fields


class HasUserPermission(BasePermission):
    def has_permission(self, request, view):
        print("Debug: HasUserPermission.has_permission called")
        if request.method == "POST":
            validate_post_fields(request=request, view=view)
        return True  # Default to allow the request

    def has_object_permission(self, request, view, obj):
        print("Debug: HasUserPermission.has_object_permission called")
        if request.method == "PATCH":
            validate_patch_fields(
                obj=obj, request=request
            )
        return True
