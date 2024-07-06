"""Summary of module

More detailed description of module
"""

from rest_framework.exceptions import ValidationError

from constants import global_admin
from constants import project_lead
from core.models import User
from core.models import UserPermissions
from core.user_cru_permissions import UserCruPermissions


class PermissionUtil:
    @staticmethod
    def get_lowest_ranked_permission_type(requesting_user: User, target_user: User):
        """Get the highest ranked permission type a requesting user has relative to a target user.

        If the requesting user is an admin, returns global_admin.

        Otherwise, it looks for the projects that both the requesting user and the serialized user are granted
        in user permissions. It then returns the highest ranked permission type that the requesting user has for
        that project.

        If the requesting user has no permissions over the serialized user, returns an empty string.

        Args:
            requesting_user (User): _description_
            target_user (User): _description_

        Returns:
            str: permission type name of highest permission type the requesting user has relative
            to the serialized user
        """

        if PermissionUtil.is_admin(requesting_user):
            return global_admin

        requesting_user_permissions = UserPermissions.objects.filter(
            user=requesting_user
        ).values("project__name", "permission_type__name", "permission_type__rank")
        target_user_projects = UserPermissions.objects.filter(user=target_user).values(
            "project__name"
        )
        lowest_permission_rank = 1000
        lowest_permission_name = ""
        for requesting_permission in requesting_user_permissions:
            lowest_permission_name, lowest_permission_rank = (
                PermissionUtil._get_lowest_rank_from_target_projects(
                    requesting_permission,
                    target_user_projects,
                    lowest_permission_rank,
                    lowest_permission_name,
                )
            )
        return lowest_permission_name

    @staticmethod
    def _get_lowest_rank_from_target_projects(
        requesting_permission,
        target_user_projects,
        lowest_permission_rank,
        lowest_permission_name,
    ):
        requesting_project_name = requesting_permission["project__name"]
        requesting_permission_name = requesting_permission["permission_type__name"]
        requesting_permission_rank = requesting_permission["permission_type__rank"]
        new_lowest_permission_name = lowest_permission_name
        new_lowest_permission_rank = lowest_permission_rank
        for target_project in target_user_projects:
            target_project_name = target_project["project__name"]
            projects_are_same = requesting_project_name == target_project_name
            rank_is_lower = requesting_permission_rank < new_lowest_permission_rank
            if projects_are_same and rank_is_lower:
                new_lowest_permission_rank = requesting_permission_rank
                new_lowest_permission_name = requesting_permission_name
        return new_lowest_permission_name, new_lowest_permission_rank

    @staticmethod
    def is_admin(user):
        """Check if user is an admin"""
        return user.is_superuser

    @staticmethod
    def has_global_admin_user_update_privs(requesting_user: User, target_user: User):
        return PermissionUtil.is_admin(requesting_user)

    @staticmethod
    def has_project_admin_user_update_privs(requesting_user: User, target_user: User):
        if PermissionUtil.is_admin(requesting_user):
            return True
        requesting_projects = UserPermissions.objects.filter(
            user=requesting_user, permission_type__name=project_lead
        ).values("project")
        serialized_projects = UserPermissions.objects.filter(user=target_user).values(
            "project"
        )
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
        highest_ranked_name = PermissionUtil.get_lowest_ranked_permission_type(
            requesting_user, target_user
        )
        print("debug highest ranked name", highest_ranked_name)
        if highest_ranked_name == "":
            raise PermissionError("You do not have permission to update this user")
        valid_fields = UserCruPermissions.update_fields[highest_ranked_name]
        if len(valid_fields) == 0:
            raise PermissionError("You do not have permission to update this user")
        print("debug valid fields", valid_fields)
        disallowed_fields = set(request_fields) - set(valid_fields)
        if disallowed_fields:
            raise ValidationError(f"Invalid fields: {', '.join(disallowed_fields)}")
