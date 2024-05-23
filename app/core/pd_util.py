from core.constants import PermissionTypeValue
from core.models import PermissionAssignment
class PdUtil:
    @staticmethod
    def is_admin(user):
        """Check if user is an admin"""
        return (user.is_superuser or 
                PermissionTypeValue.global_admin in PermissionAssignment.objects.filter(
                    user=user).values_list('permission_type__name', flat=True)
        )
    
    
    @staticmethod
    def can_read_secure(requesting_user, serialized_user):
        """Check if requesting user can see secure user info"""
        if PdUtil.is_admin(requesting_user):
            return True
        requesting_projects = PermissionAssignment.objects.filter(
            user = requesting_user,
            permission_type__name=PermissionTypeValue.project_lead).values(
                "project").distinct()
        serialized_projects = PermissionAssignment.objects.filter(
            user = serialized_user).values(
                "project").distinct() 
        return requesting_projects.intersection(serialized_projects).exists()       

    @staticmethod
    def can_read_basic(requesting_user, serialized_user):
        requesting_projects = PermissionAssignment.objects.filter(user = requesting_user).values("project")
        serialized_projects = PermissionAssignment.objects.filter(user = serialized_user).values("project")
        return requesting_projects.intersection(serialized_projects).exists()       
