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
        in user permissions. It then returns the permission type name of the lowest ranked matched permission.

        If the requesting user has no permissions over the serialized user, returns an empty string.

        Args:
            requesting_user (User): user that initiates the API request
            target_user (User): a user that is part of the API response currently being serialized

        Returns:
            str: permission type name of highest permission type the requesting user has relative
            to the serialized user
        """

        if PermissionUtil.is_admin(requesting_user):
            return global_admin

        target_user_project_names = UserPermissions.objects.filter(
            user=target_user
        ).values_list("project__name", flat=True)

        matched_requester_permissions = UserPermissions.objects.filter(
            user=requesting_user, project__name__in=target_user_project_names
        ).values("permission_type__name", "permission_type__rank")

        lowest_permission_rank = 1000
        lowest_permission_name = ""
        for matched_permission in matched_requester_permissions:
            matched_permission_rank = matched_permission["permission_type__rank"]
            matched_permission_name = matched_permission["permission_type__name"]
            if matched_permission_rank < lowest_permission_rank:
                lowest_permission_rank = matched_permission_rank
                lowest_permission_name = matched_permission_name

        return lowest_permission_name

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
