from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied

class DenyAny(BasePermission):
    def has_permission(self, request, view):
        return False

    def has_object_permission(self, request, view, obj):
        return False

class UserAppKbPermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        exists = user.groups.filter(name__startswith="kb_").exists()
        return exists
        
    def has_object_permission(self, request, view, obj):
        exists = obj.groups.filter(name__startswith="kb_").exists()
        return exists
