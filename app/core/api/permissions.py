from rest_framework.permissions import BasePermission
import json


class DenyAny(BasePermission):
    def has_permission(self, request, view):
        return False

    def has_object_permission(self, request, view, obj):
        return False


class IsAuthenticated2(BasePermission):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):
        print("debug", json.stringify(request.user))
        return bool(request.user and request.user.is_authenticated)
