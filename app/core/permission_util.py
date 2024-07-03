from rest_framework.exceptions import ValidationError

from core.user_cru_permissions import UserCruPermissions
from constants import global_admin, project_lead, practice_area_admin
from core.models import UserPermissions
from core.models import User


class PermissionUtil:
    @staticmethod
    def is_admin(user):
        """Check if user is an admin"""
        return user.is_superuser

    @staticmethod
    def can_read_all_user(requesting_user: User, serialized_user: User):
        """Check if requesting user can see secure user info"""
        if (
            PermissionUtil.is_admin(requesting_user)
            or requesting_user == serialized_user
        ):
            return True
        requesting_projects = (
            UserPermissions.objects.filter(
                user=requesting_user,
                permission_type__name=project_lead,
            )
            .values("project")
            .distinct()
        )
        serialized_projects = (
            UserPermissions.objects.filter(user=serialized_user)
            .values("project")
            .distinct()
        )
        return requesting_projects.intersection(serialized_projects).exists()

    @staticmethod
    def can_read_basic_user(requesting_user: User, serialized_user: User):
        if PermissionUtil.is_admin(requesting_user):
            return True
        requesting_projects = UserPermissions.objects.filter(
            user=requesting_user
        ).values("project")
        serialized_projects = UserPermissions.objects.filter(
            user=serialized_user
        ).values("project")
        return requesting_projects.intersection(serialized_projects).exists()

    @staticmethod
    def has_global_admin_user_update_privs(
        requesting_user: User, serialized_user: User
    ):
        return PermissionUtil.is_admin(requesting_user)

    @staticmethod
    def has_project_admin_user_update_privs(
        requesting_user: User, serialized_user: User
    ):
        if PermissionUtil.is_admin(requesting_user):
            return True
        requesting_projects = UserPermissions.objects.filter(
            user=requesting_user, permission_type__name=project_lead
        ).values("project")
        serialized_projects = UserPermissions.objects.filter(
            user=serialized_user
        ).values("project")
        return requesting_projects.intersection(serialized_projects).exists()

    @staticmethod
    def validate_update_request(request):
        request_fields = request.json().keys()
        requesting_user = request.context.get("request").user
        target_user = User.objects.get(uuid=request.context.get("uuid"))
        PermissionUtil.validate_fields_updateable(
            requesting_user, target_user, request_fields
        )

    @staticmethod
    def validate_fields_updateable(requesting_user, target_user, request_fields):
        if PermissionUtil.has_global_admin_user_update_privs(
            requesting_user, target_user
        ):
            valid_fields = UserCruPermissions.update_fields["user"][global_admin]
        elif PermissionUtil.has_project_admin_user_update_privs(
            requesting_user, target_user
        ):
            valid_fields = UserCruPermissions.update_fields["user"][practice_area_admin]
        else:
            raise PermissionError("You do not have permission to update this user")
        disallowed_fields = set(request_fields) - set(valid_fields)
        if disallowed_fields:
            raise ValidationError(f"Invalid fields: {', '.join(disallowed_fields)}")
