import csv
import sys
from functools import lru_cache
from typing import Any, Dict, List
from rest_framework.exceptions import ValidationError, PermissionDenied
from constants import field_permissions_csv_file, admin_global  # Assuming you have this constant
from core.models import PermissionType, UserPermission

class FieldPermissionCheck:

    @staticmethod
    def is_admin(user) -> bool:
        """Check if a user has admin permissions."""
        permission_type = PermissionType.objects.filter(name=admin_global).first()
        print("Debug", permission_type, "x", user, flush=True, file=sys.stdout)
        # return True
        return UserPermission.objects.filter( # huh?
            permission_type=permission_type, user=user
        ).exists()

    @staticmethod
    @lru_cache
    def get_rank_dict() -> Dict[str, int]:
        """Return a dictionary mapping permission names to their ranks."""
        permissions = PermissionType.objects.values("name", "rank")
        return {perm["name"]: perm["rank"] for perm in permissions}

    @staticmethod
    @lru_cache
    def csv_field_permissions() -> Dict[str, Dict[str, List[Dict[str, Any]]]]:
        """Read the field permissions from a CSV file."""
        with open(field_permissions_csv_file, mode="r", newline="") as file:
            reader = csv.DictReader(file)
            return list(reader)

    @classmethod
    def role_field_permissions(cls, operation: str, permission_type: str, table_name: str) -> List[str]:
        """Return the valid fields for the given permission type."""
        rank_dict = cls.get_rank_dict()
        source_rank = rank_dict[permission_type]
        valid_fields = []
        for field in cls.csv_field_permissions():
            operation_match = field[operation] == operation
            table_match = field[table_name] == table_name
            rank_match = rank_dict[permission_type] >= source_rank

            if operation_match and table_match and rank_match:
                field["table_name"] == table_name                
                valid_fields += [field["field_name"]]

    @classmethod
    def get_most_privileged_perm_type(
        cls, requesting_user, target_user
    ) -> str:
        """Return the most privileged permission type between users."""
        if cls.is_admin(requesting_user):
            return admin_global

        target_projects = UserPermission.objects.filter(user=target_user).values_list(
            "project__name", flat=True
        )

        permissions = UserPermission.objects.filter(
            user=requesting_user, project__name__in=target_projects
        ).values("permission_type__name", "permission_type__rank")

        if not permissions:
            return ""

        min_permission = min(permissions, key=lambda p: p["permission_type__rank"])
        return min_permission["permission_type__name"]

    @classmethod
    def validate_user_fields_patchable(
        cls, requesting_user, target_user, request_fields: List[str]
    ) -> None:
        """Ensure the requesting user can patch the provided fields."""
        most_privileged_perm_type = cls.get_most_privileged_perm_type(requesting_user, target_user)
        valid_fields = cls.role_field_permissions(
            operation = "update", 
            table_name = "user", 
            permission_type = most_privileged_perm_type
        )
        disallowed_fields = set(request_fields) - set(valid_fields)

        if not valid_fields:
            raise PermissionDenied(f"You do not have update privileges ")
        elif valid_fields - disallowed_fields:
            raise ValidationError(f"Invalid fields: {', '.join(disallowed_fields)}")

    @classmethod
    def clear(cls) -> None:
        """Clear the cached field permissions."""
        cls.csv_field_permissions.cache_clear()
        cls.get_rank_dict.cache_clear()
