import csv
from pathlib import Path
from typing import Any
import pytest
from rest_framework.exceptions import PermissionDenied

from constants import ADMIN_GLOBAL  # Assuming you have this constant
from constants import FIELD_PERMISSIONS_CSV
from core.models import PermissionType
from core.models import UserPermission

@pytest.mark.load_user_data_required
class PermissionValidation:
    """A collection of static methods for validating user permissions."""

    @staticmethod
    def is_admin(user) -> bool:
        """Check if a user assigned "globalAdmin" permission."""
        permission_type = PermissionType.objects.filter(name=ADMIN_GLOBAL).first()
        # return True
        return UserPermission.objects.filter(
            permission_type=permission_type, user=user
        ).exists()

    @staticmethod
    def get_rank_dict() -> dict[str, int]:
        """Return a dictionary mapping permission names to their ranks.
        Example: {"adminGlobal": 1, "adminProject": 2, "practiceLeadProject": 3, "memberProject": 4}.
        Used in algorithm to determine most privileged permission type between two users.  The lower the rank,
        the more privileged the permission.
        """
        permissions = PermissionType.objects.values("name", "rank")
        return {perm["name"]: perm["rank"] for perm in permissions}

    @staticmethod
    def get_csv_field_permissions() -> dict[str, dict[str, list[dict[str, Any]]]]:
        """Read the field permissions from a CSV file.
        Returns a list of dictionaries, each representing a row in the CSV file.
        Each dictionary contains key values for: table_name, field_name, get, post, patch.
        """
        file_path = Path(FIELD_PERMISSIONS_CSV)
        with file_path.open() as file:
            reader = csv.DictReader(file)
            return list(reader)

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

        print("debug operation, permission_type, table_name", operation, permission_type, table_name)  # --- IGNORE ---
        for field_permission in cls.get_csv_field_permissions():
            print("debug field_permission", field_permission["field_name"], field_permission[operation],)  # --- IGNORE ---
            if cls.has_field_permission(
                operation=operation,
                requester_permission_type=permission_type,
                table_name=table_name,
                field=field_permission,
            ):
                valid_fields.add(field_permission["field_name"])

        return list(valid_fields)

    @classmethod
    def get_fields_for_post_request(cls, request, table_name):
        requesting_user = request.user
        if not cls.is_admin(requesting_user):
            raise PermissionDenied("You do not have privilges to create.")
        fields = cls.get_permitted_fields(
            operation="post",
            table_name=table_name,
            permission_type=ADMIN_GLOBAL,
        )
        return fields

    @classmethod
    def get_fields_for_patch_request(cls, request, table_name, response_related_user):
        requesting_user = request.user
        requesting_user = request.user
        most_privileged_perm_type = cls.get_most_privileged_perm_type(
            requesting_user, response_related_user
        )
        fields = cls.get_permitted_fields(
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
        fields = cls.get_permitted_fields(
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
    def get_response_fields(cls, request, table_name, response_related_user) -> None:
        """Ensure the requesting user can patch the provided fields."""
        requesting_user = request.user
        most_privileged_perm_type = cls.get_most_privileged_perm_type(
            requesting_user, response_related_user
        )
        fields = cls.get_permitted_fields(
            operation="get",
            table_name=table_name,
            permission_type=most_privileged_perm_type,
        )
        return fields

    @classmethod
    def has_field_permission(
        cls, operation: str, requester_permission_type: str, table_name: str, field: dict
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
        print("debug checking field permission for name, operation, requester_permission_type, operation look up", field.get("field_name"), operation, requester_permission_type, field.get(operation))  # --- IGNORE ---
        operation_permission_type = field.get(operation, "")
        if not operation_permission_type or field.get("table_name") != table_name:
            print("debug no permission type or table name mismatch")  # --- IGNORE ---
            return False

        rank_dict = cls.get_rank_dict()
        if (
            requester_permission_type not in rank_dict
            or operation_permission_type not in rank_dict
        ):
            print("debug no requester_permission_type or operation_permission_type")  # --- IGNORE ---
            return False
        print("debug ranks", rank_dict[requester_permission_type], rank_dict[operation_permission_type])  # --- IGNORE ---
        print("returning", rank_dict[requester_permission_type] >= rank_dict[operation_permission_type])  # --- IGNORE ---

        return rank_dict[requester_permission_type] >= rank_dict[operation_permission_type]
