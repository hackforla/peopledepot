from core.constants import PermissionTypeValue
from core.models import PermissionAssignment, User
from .constants import project_lead, update_fields

class PermissionUtil:
    @staticmethod
    def is_admin(user):
        """Check if user is an admin"""
        return (user.is_superuser or 
                PermissionTypeValue.global_admin in PermissionAssignment.objects.filter(
                    user=user).values_list('permission_type__name', flat=True)
        )
    
    
    @staticmethod
    def can_read_user_secure(requesting_user: User, serialized_user: User):
        """Check if requesting user can see secure user info"""
        if PermissionUtil.is_admin(requesting_user) or requesting_user == serialized_user:
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
    def can_read_user_basic(requesting_user: User, serialized_user: User):
        if PermissionUtil.is_admin(requesting_user):
            return True
        requesting_projects = PermissionAssignment.objects.filter(user = requesting_user).values("project")
        serialized_projects = PermissionAssignment.objects.filter(user = serialized_user).values("project")
        return requesting_projects.intersection(serialized_projects).exists()       

    @staticmethod
    def can_update_user_admin(requesting_user: User, serialized_user: User):
        return PermissionUtil.is_admin(requesting_user)

    @staticmethod
    def can_update_user_lead(requesting_user: User, serialized_user: User):
        if PermissionUtil.is_admin(requesting_user):
            return True
        requesting_projects = PermissionAssignment.objects.filter(user = requesting_user, permission_type__name = project_lead).values("project")
        serialized_projects = PermissionAssignment.objects.filter(user = serialized_user).values("project")
        return requesting_projects.intersection(serialized_projects).exists()       

    @staticmethod
    def validate_request_fields(request):
        request_fields = request.json().keys()
        requesting_user = request.context.get("request").user
        target_user = User.objects.get(uuid=request.context.get("uuid"))
        PermissionUtil.validate_fields(requesting_user, target_user, request_fields)

    @staticmethod 
    def validate_fields(requesting_user, target_user, request_fields):
        if PermissionUtil.can_update_user_admin(requesting_user, target_user):
            valid_fields = update_fields["user"]["admin"]
        elif PermissionUtil.can_update_user_lead(requesting_user, target_user):
            valid_fields = update_fields["user"]["lead"]
        else:
            raise PermissionError("You do not have permission to update this user")
        disallowed_fields = set(request_fields) - set(valid_fields)
        return disallowed_fields is None
        
        
        