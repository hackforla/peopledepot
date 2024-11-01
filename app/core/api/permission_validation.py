import csv
from typing import Any

from rest_framework.exceptions import PermissionDenied
from pathlib import Path

from constants import admin_global  # Assuming you have this constant
from constants import field_permissions_csv_file
from core.models import PermissionType
from core.models import UserPermission


class PermissionValidation:
    @staticmethod
    def is_admin(user) -> bool:
        """Check if a user has admin permissions."""
        permission_type = PermissionType.objects.filter(name=admin_global).first()
        # return True
        return UserPermission.objects.filter(
            permission_type=permission_type, user=user
        ).exists()

    @staticmethod
    def get_rank_dict() -> dict[str, int]:
        """Return a dictionary mapping permission names to their ranks."""
        permissions = PermissionType.objects.values("name", "rank")
        return {perm["name"]: perm["rank"] for perm in permissions}

    @staticmethod
    def get_csv_field_permissions() -> dict[str, dict[str, list[dict[str, Any]]]]:
        """Read the field permissions from a CSV file."""
        file_path = Path(field_permissions_csv_file)
        with file_path.open() as file:
            reader = csv.DictReader(file)
            return list(reader)

    @classmethod
    def get_fields(
        cls, operation: str, permission_type: str, table_name: str
    ) -> list[str]:
        """Return the valid fields for the given permission type."""

        valid_fields = []
        if permission_type == "":
            return valid_fields
        for field in cls.get_csv_field_permissions():
            if cls.is_field_valid(
                operation=operation,
                permission_type=permission_type,
                table_name=table_name,
                field=field,
            ):
                valid_fields += [field["field_name"]]
        return valid_fields

    # todo: refactor to change request to requesting_user?
    @classmethod
    def get_fields_for_post_request(cls, request, table_name):
        requesting_user = request.user
        if not cls.is_admin(requesting_user):
            raise PermissionDenied("You do not have privilges to create.")
        fields = cls.get_fields(
            operation="post",
            table_name=table_name,
            permission_type=admin_global,
        )
        return fields

    @classmethod
    @classmethod
    def get_fields_for_patch_request(cls, request, table_name, response_related_user):
        requesting_user = request.user
        requesting_user = request.user
        most_privileged_perm_type = cls.get_most_privileged_perm_type(
            requesting_user, response_related_user
        )
        fields = cls.get_fields(
            operation="patch",
            table_name=table_name,
            permission_type=most_privileged_perm_type,
        )
        return fields

    @classmethod
    def get_fields_for_response(cls, request, table_name, response_related_user):
        requesting_user = request.user
        most_privileged_perm_type = cls.get_most_privileged_perm_type(
            requesting_user, response_related_user
        )
        fields = cls.get_fields(
            operation="get",
            table_name=table_name,
            permission_type=most_privileged_perm_type,
        )
        return fields

    @classmethod
    def get_most_privileged_perm_type(
        cls, requesting_user, response_related_user
    ) -> str:
        """Return the most privileged permission type between users."""
        if cls.is_admin(requesting_user):
            return admin_global

        target_projects = UserPermission.objects.filter(
            user=response_related_user
        ).values_list("project__name", flat=True)
        target_projects = UserPermission.objects.filter(
            user=response_related_user
        ).values_list("project__name", flat=True)

        permissions = UserPermission.objects.filter(
            user=requesting_user, project__name__in=target_projects
        ).values("permission_type__name", "permission_type__rank")

        if not permissions:
            return ""

        min_permission = min(permissions, key=lambda p: p["permission_type__rank"])
        return min_permission["permission_type__name"]

    @classmethod
    def get_response_fields(cls, request, table_name, response_related_user) -> None:
        """Ensure the requesting user can patch the provided fields."""
        requesting_user = request.user
        most_privileged_perm_type = cls.get_most_privileged_perm_type(
            requesting_user, response_related_user
        )
        fields = cls.get_fields(
            operation="get",
            table_name=table_name,
            permission_type=most_privileged_perm_type,
        )
        return fields

    @classmethod
    def is_field_valid(
        cls, operation: str, permission_type: str, table_name: str, field: dict
    ):
        operation_permission_type = field[operation]
        if operation_permission_type == "" or field["table_name"] != table_name:
            return False
        rank_dict = cls.get_rank_dict()
        source_rank = rank_dict[permission_type]
        source_rank = rank_dict[permission_type]
        rank_match = source_rank <= rank_dict[operation_permission_type]
        return rank_match
