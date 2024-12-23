from rest_framework.permissions import BasePermission


class DenyAny(BasePermission):
    def has_permission(self, request, view):
        return False

    def has_object_permission(self, request, view, obj):
        return False

# kb_admin  view_basic_user_info
# kb_user

class UserAppPermission(BasePermission):
    def has_permission(self, request, __view__):
        return request.user.has_perm("view_api_user_basic")
    
class AppUserPermission(BasePermission):
    def has_permission(self, request, __view__):
        return request.user.has_perm("view_api_user_app")
    
    def has_object_permission(self, request, view, obj):
        if not request.user.has_perm("view_api_user_app"):
            return False
        # TODO: find if any privileges with ""
        return super().has_object_permission(request, view, obj)