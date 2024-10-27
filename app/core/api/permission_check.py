import csv
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
        # return True
        return UserPermission.objects.filter( # 
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
    def csv_field_permissions() -> List[Dict[str, str]]:
        """Read the field permissions from a CSV file."""

    @classmethod
    def is_field_valid(cls, operation: str, permission_type: str, table_name: str, field: Dict):
        operation_permission_type = field[operation]
        if operation_permission_type == "" or field["table_name"] != table_name:
            return False
        rank_dict = cls.get_rank_dict()
        source_rank = rank_dict[permission_type]            
        rank_match = source_rank <= rank_dict[operation_permission_type]
        return rank_match

    @classmethod
    def get_valid_fields(cls, operation: str, permission_type: str, table_name: str) -> List[str]:
        """Return the valid fields for the given permission type."""

        valid_fields = []
        for field in cls.csv_field_permissions():
            if cls.is_field_valid(operation=operation, permission_type=permission_type, table_name=table_name, field=field):
                valid_fields += [field["field_name"]]
        return valid_fields

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
    def validate_fields_for_target_user(
        cls, operation, table_name, requesting_user, target_user, request_fields: List[str]
    ) -> None:
        """Ensure the requesting user can patch the provided fields."""
        most_privileged_perm_type = cls.get_most_privileged_perm_type(requesting_user, target_user)
        valid_fields = cls.get_valid_fields(
            operation = operation, 
            table_name = table_name, 
            permission_type = most_privileged_perm_type
        )
        disallowed_fields = set(request_fields) - set(valid_fields)

        if not valid_fields:
            raise PermissionDenied(f"You do not have update privileges ")
        elif disallowed_fields:
            raise ValidationError(f"Invalid fields: {', '.join(disallowed_fields)}")

    @classmethod
    def clear(cls) -> None:
        """Clear the cached field permissions."""
        cls.csv_field_permissions.cache_clear()
        cls.get_rank_dict.cache_clear()
