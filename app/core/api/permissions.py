from rest_framework.permisisons import BasePermission


class DenyAny(BasePermission):
    def has_permission(self, request, view):
        return False

    def has_object_permission(self, request, view, obj):
        return False
