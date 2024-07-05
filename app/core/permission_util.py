from rest_framework.exceptions import ValidationError

from constants import global_admin
from constants import practice_area_admin
from constants import project_lead
from core.models import User
from core.models import UserPermissions
from core.user_cru_permissions import UserCruPermissions


class PermissionUtil:
    @staticmethod
    def get_highest_ranked_permission_type(
        requesting_user: User, serialized_user: User
    ):
        if PermissionUtil.is_admin(requesting_user):
            return global_admin

        requesting_projects = UserPermissions.objects.filter(
            user=requesting_user
        ).values("project__name", "permission_type__name", "permission_type__rank")
        serialized_projects = UserPermissions.objects.filter(
            user=serialized_user
        ).values("project__name")
        highest_ranked_permission = 1000
        highest_ranked_name = ""
        for requesting_project in requesting_projects:
            for serialized_project in serialized_projects:
                if (
                    requesting_project["project__name"]
                    == serialized_project["project__name"]
                ):
                    if (
                        requesting_project["permission_type__rank"]
                        < highest_ranked_permission
                    ):
                        highest_ranked_permission = requesting_project[
                            "permission_type__rank"
                        ]
                        highest_ranked_name = requesting_project[
                            "permission_type__name"
                        ]
        return highest_ranked_name

    @staticmethod
    def is_admin(user):
        """Check if user is an admin"""
        return user.is_superuser

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
            valid_fields = UserCruPermissions.update_fields[global_admin]
        elif PermissionUtil.has_project_admin_user_update_privs(
            requesting_user, target_user
        ):
            valid_fields = UserCruPermissions.update_fields[practice_area_admin]
        else:
            raise PermissionError("You do not have permission to update this user")
        disallowed_fields = set(request_fields) - set(valid_fields)
        if disallowed_fields:
            raise ValidationError(f"Invalid fields: {', '.join(disallowed_fields)}")
