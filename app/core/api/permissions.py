from rest_framework.permissions import BasePermission


class DenyAny(BasePermission):
    def has_permission(self, request, view) -> bool:
        return False

    def has_object_permission(self, request, view, obj) -> bool:
        return False

