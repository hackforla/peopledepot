import csv
from pathlib import Path
from typing import Any

from rest_framework.exceptions import PermissionDenied

from constants import admin_global, field_permissions_csv_file
from core.models import PermissionType, UserPermission


class PermissionValidation:
    """Utility methods for validating user permissions and field-level access."""

    # ---------- Admin Check ----------

    @staticmethod
    def is_admin(user) -> bool:
        """Return whether the user has the global admin permission.

        :param user: The user object being checked.
        :return: ``True`` if the user has the ``globalAdmin`` permission, else ``False``.

        """
        permission_type = PermissionType.objects.filter(name=admin_global).first()
        return UserPermission.objects.filter(
            permission_type=permission_type, user=user
        ).exists()

    # ---------- Rank Utilities ----------

    @staticmethod
    def get_rank_dict() -> dict[str, int]:
        """Return a dictionary mapping permission type names to rank values.

        The lower the rank value, the more privileged the permission.

        :return: A dictionary where keys are permission names and values are rank integers.

        Example::

            >>> PermissionValidation.get_rank_dict()
            {"adminGlobal": 1, "adminProject": 2, "memberProject": 3}
        """
        return {
            perm["name"]: perm["rank"]
            for perm in PermissionType.objects.values("name", "rank")
        }

    # ---------- CSV Utilities ----------

    @staticmethod
    def get_csv_field_permissions() -> list[dict[str, Any]]:
        """Load field permissions from a CSV file.

        Each row in the CSV represents one field and the permissions required for
        different operations (e.g., GET, POST, PATCH).

        :return: A list of dictionaries. Each dictionary contains at least:

            * ``table_name`` (str)
            * ``field_name`` (str)
            * operation-specific permissions (e.g., ``get``, ``post``, ``patch``)

        Example row::

            {
                "table_name": "User",
                "field_name": "email",
                "get": "memberProject",
                "post": "adminProject",
                "patch": "adminGlobal"
            }
        """
        file_path = Path(field_permissions_csv_file)
        with file_path.open() as file:
            return list(csv.DictReader(file))

    # ---------- Core Permission Logic ----------

    @classmethod
    def get_permitted_fields(
        cls, operation: str, permission_type: str, table_name: str
    ) -> list[str]:
        """Return permitted field names for a given operation.

        This checks the CSV configuration and determines which fields
        are accessible to a user based on their permission type.

        :param operation: The type of operation, e.g., ``"get"``, ``"post"``, or ``"patch"``.
        :param permission_type: The permission type of the user
            (e.g., ``"adminGlobal"``, ``"adminProject"``).
        :param table_name: The database table or model name (e.g., ``"User"``).
        :return: A list of field names permitted for the given operation.

        Example::

            >>> PermissionValidation.get_permitted_fields("get", "adminProject", "User")
            ["first_name", "last_name"]
        """
        if not permission_type:
            return []

        valid_fields = set()

        for field_permission in cls.get_csv_field_permissions():
            if cls.has_field_permission(
                operation=operation,
                permission_type=permission_type,
                table_name=table_name,
                field=field_permission,
            ):
                valid_fields.add(field_permission["field_name"])

        return list(valid_fields)

    @classmethod
    def has_field_permission(
        cls, operation: str, permission_type: str, table_name: str, field: dict
    ) -> bool:
        """Check if a permission type allows access to a field.

        :param operation: The type of operation, e.g., ``"get"``, ``"post"``, ``"patch"``.
        :param permission_type: The permission type of the user (e.g., ``"adminProject"``).
        :param table_name: The table/model name to check (e.g., ``"User"``).
        :param field: A dictionary describing the field, including at least:

            * ``table_name``
            * ``field_name``
            * operation-specific permission values (e.g., ``{"get": "adminProject"}``)

        :return: ``True`` if the permission type allows access to the field, otherwise ``False``.

        Example::

            >>> field_info = {
            ...     "table_name": "User",
            ...     "field_name": "email",
            ...     "get": "adminProject"
            ... }
            >>> PermissionValidation.has_field_permission("get", "adminProject", "User", field_info)
            True
        """
        operation_perm_type = field.get(operation)
        if not operation_perm_type or field.get("table_name") != table_name:
            return False

        rank_dict = cls.get_rank_dict()
        return (
            permission_type in rank_dict
            and operation_perm_type in rank_dict
            and rank_dict[permission_type] <= rank_dict[operation_perm_type]
        )

    # ---------- Request-Oriented Field Getters ----------

    @classmethod
    def get_fields_for_post_request(cls, request, table_name) -> list[str]:
        """Return permitted fields for a POST request.

        Only admins may create records. Raises ``PermissionDenied`` otherwise.

        :param request: The request object containing the user.
        :param table_name: The table/model name.
        :return: A list of permitted field names for POST operations.
        """
        if not cls.is_admin(request.user):
            raise PermissionDenied("You do not have privileges to create.")
        return cls.get_permitted_fields("post", admin_global, table_name)

    @classmethod
    def get_fields_for_patch_request(cls, request, table_name, response_related_user):
        """Return permitted fields for a PATCH request.

        :param request: The request object containing the requesting user.
        :param table_name: The table/model name.
        :param response_related_user: The user whose data is being modified.
        :return: A list of permitted field names for PATCH operations.
        """
        perm_type = cls.get_most_privileged_perm_type(request.user, response_related_user)
        return cls.get_permitted_fields("patch", perm_type, table_name)

    @classmethod
    def get_fields_for_get_request(cls, request, table_name, response_related_user):
        """Return permitted fields for a GET request (response data).

        :param request: The request object containing the requesting user.
        :param table_name: The table/model name.
        :param response_related_user: The user whose data is being accessed.
        :return: A list of permitted field names for GET operations.
        """
        perm_type = cls.get_most_privileged_perm_type(request.user, response_related_user)
        return cls.get_permitted_fields("get", perm_type, table_name)

    # ---------- Privilege Comparison ----------

    @classmethod
    def get_most_privileged_perm_type(cls, requesting_user, response_related_user) -> str:
        """Return the most privileged permission type between two users.

        If the requesting user is a global admin, ``adminGlobal`` is returned.
        Otherwise, the function finds the lowest-ranked permission shared
        across the projects of the two users.

        :param requesting_user: The user making the request.
        :param response_related_user: The user whose data is being accessed.
        :return: The name of the most privileged permission type, or an empty string if none found.
        """
        if cls.is_admin(requesting_user):
            return admin_global

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
