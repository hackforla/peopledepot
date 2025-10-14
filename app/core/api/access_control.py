import csv
from pathlib import Path
from typing import Any

from rest_framework.exceptions import PermissionDenied

from constants import ADMIN_GLOBAL  # Assuming you have this constant
from constants import FIELD_PERMISSIONS_CSV
from core.models import PermissionType
from core.models import UserPermission


class AccessControl:
    """A collection of static methods for validating user permissions."""

    _rank_dict_cache: dict[str, int] | None = None  # class-level cache
    _csv_field_permissions_cache: list[dict[str, Any]] | None = None

    @staticmethod
    def is_admin(user) -> bool:
        """Check if a user assigned "adminGlobal" permission."""
        permission_type = PermissionType.objects.filter(name=ADMIN_GLOBAL).first()
        # return True
        return UserPermission.objects.filter(
            permission_type=permission_type, user=user
        ).exists()

    @classmethod
    def _get_rank_dict(cls) -> dict[str, int]:
        """Return a dictionary mapping permission names to their ranks.
        Example: {"adminGlobal": 1, "adminProject": 2, "practiceLeadProject": 3, "memberProject": 4}.
        Used in algorithm to determine most privileged permission type between two users.  The higher the rank,
        the more privileged the permission.
        """
        if cls._rank_dict_cache is None:
            permissions = PermissionType.objects.values("name", "rank")
            cls._rank_dict_cache = {perm["name"]: perm["rank"] for perm in permissions}
        return cls._rank_dict_cache

    @classmethod
    def _get_csv_field_permissions(cls) -> list[dict[str, Any]]:
        """Read the field permissions from a CSV file.

        Caches the result so the CSV is read only once.
        """
        if cls._csv_field_permissions_cache is None:
            file_path = Path(FIELD_PERMISSIONS_CSV)
            with file_path.open() as file:
                reader = csv.DictReader(file)
                cls._csv_field_permissions_cache = list(reader)
        return cls._csv_field_permissions_cache

    @classmethod
    def get_permitted_fields(
        cls, operation: str, permission_type: str, table_name: str
    ) -> list[str]:
        """
        Return the list of field names accessible for a user with the given permission type
        for a given operation.

        Parameters:
            operation (str): The type of operation. (e.g., "get", "post", "patch").
            permission_type (str): The permission type of the requesting user
                (e.g., "adminGlobal", "adminProject", etc.).
            table_name (str): The name of the table/model
                (e.g., "User", "Project").

        Returns:
            list[str]: A list of field names that the user with the given
            permission_type can access for the specified operation on the
            specified table.

        Example:
            >>> get_fields("get", "adminProject", "User")
            ["first_name", "last_name"]
        """
        if not permission_type:  # Early exit guard clause
            return []

        valid_fields = set()

        for field_permission in cls._get_csv_field_permissions():
            if cls.has_field_permission(
                operation=operation,
                requester_permission_type=permission_type,
                table_name=table_name,
                field=field_permission,
            ):
                valid_fields.add(field_permission["field_name"])

        return list(valid_fields)

    @classmethod
    def get_highest_user_perm_type(
        cls, requesting_user
    ) -> str:
        """Return the most privileged permission type of a user."""



        permissions = UserPermission.objects.filter(
            user=requesting_user, project__name=None
        ).values("permission_type__name", "permission_type__rank")

        if not permissions:
            return ""

        max_permission = max(permissions, key=lambda p: p["permission_type__rank"])
        return max_permission["permission_type__name"]

    @classmethod
    def get_highest_shared_project_perm_type(
        cls, requesting_user, response_related_user
    ) -> str:
        """Return the most privileged permission type between users."""
        if cls.is_admin(requesting_user):
            return ADMIN_GLOBAL

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

        max_permission = max(permissions, key=lambda p: p["permission_type__rank"])
        return max_permission["permission_type__name"]

    @classmethod
    def has_field_permission(
        cls,
        operation: str,
        requester_permission_type: str,
        table_name: str,
        field: dict,
    ) -> bool:
        """
        Determine whether a user with a given permission type has access to a field
        for a specific operation on a specific table.

        Parameters:
            operation (str): The type of operation ("get", "post", or "patch").
            permission_type (str): The user's permission type
                (e.g., "adminGlobal", "adminProject").
            table_name (str): The name of the table/model to check (e.g., "User").
            field (dict): A dictionary describing the field, including at least:
                - "field_name"
                - "table_name"
                - operation-specific permission values
                  (e.g., {"get": "adminProject"}).

        Returns:
            bool: True if the permission type allows access to the field for the operation,
            False otherwise.

        Example:
            >>> field_info = {
            ...     "field_name": "email",
            ...     "table_name": "User",
            ...     "get": "adminProject"
            ... }
            >>> has_field_permission("get", "adminProject", "User", field_info)
            True
        """
        operation_permission_type = field.get(operation, "")
        if not operation_permission_type or field.get("table_name") != table_name:
            return False

        rank_dict = cls._get_rank_dict()
        if (
            requester_permission_type not in rank_dict
            or operation_permission_type not in rank_dict
        ):
            return False
        return (
            rank_dict[requester_permission_type] <= rank_dict[operation_permission_type]
        )
