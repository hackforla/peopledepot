from core.api.user_related_request import UserRelatedRequest
from rest_framework.permissions import BasePermission


class HasUserPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST":
            UserRelatedRequest.validate_post_fields(request=request, view=view)
        return True  # Default to allow the request

    def has_object_permission(self, request, view, obj):
        print("HasUserPermission.has_object_permission called")
        if request.method == "PATCH":
            UserRelatedRequest.validate_patch_fields(
                view=view, obj=obj, request=request
            )
        return True