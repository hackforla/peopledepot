import csv
import inspect
from functools import lru_cache
from typing import Any, Dict, List
from rest_framework.exceptions import ValidationError, PermissionDenied, MethodNotAllowed
from constants import field_permissions_csv_file, admin_global  # Assuming you have this constant
from core.models import PermissionType, UserPermission

class FieldPermissionCheck:

    @staticmethod
    def clear_all_caches(module):
        """Clear all lru_cache decorated functions in a given module."""
        for __name__, func in inspect.getmembers(module, inspect.isfunction):
            if hasattr(func, "cache_clear"):
                func.cache_clear()

    @ staticmethod
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
    def get_csv_field_permissions() -> Dict[str, Dict[str, List[Dict[str, Any]]]]:
        """Read the field permissions from a CSV file."""
        with open(field_permissions_csv_file, mode="r", newline="") as file:
            reader = csv.DictReader(file)
            return list(reader)

    @classmethod
    def get_fields(
        cls, operation: str, permission_type: str, table_name: str
    ) -> List[str]:
        """Return the valid fields for the given permission type."""

        valid_fields = []
        for field in cls.get_csv_field_permissions():
            if cls.is_field_valid(
                operation=operation,
                permission_type=permission_type,
                table_name=table_name,
                field=field,
            ):
                valid_fields += [field["field_name"]]
        print("debug 2", valid_fields)
        return valid_fields

    @classmethod
    def get_fields_for_request(cls, request, operation, table_name, target_user):
        requesting_user = request.user
        most_privileged_perm_type = cls.get_most_privileged_perm_type(
            requesting_user, target_user
        )
        fields = cls.get_fields(
                operation=operation,
                table_name=table_name,
                permission_type=most_privileged_perm_type
        )
        return fields

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

    def get_response_fields(cls, request, target_obj) -> None:
        """Ensure the requesting user can patch the provided fields."""
        print("debug", request)
        return cls.get_fields_for_request(
            operation="read",
            table_name="user",
            request=request,
            target_user=target_obj
        )

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
    def clear_all_caches(cls) -> None:
        """Clear the cached field permissions."""

    @classmethod
    def validate_request_on_target_user(cls, request, target_user) -> None:
        """Ensure the requesting user can patch the provided fields."""
        method = request.method.lower()
        if request.method not in ("PATCH", "POST"):
            raise MethodNotAllowed("Application error.")
        valid_fields = cls.get_fields_for_request(
            operation=method.lower(),
            table_name="user",
            request=request,
            target_user=target_user
        )
        print("debug", valid_fields, "xxxx")
        request_data_keys = set(request.data)
        disallowed_fields = request_data_keys - set(valid_fields)

        if not valid_fields:
            raise PermissionDenied(f"You do not have update privileges ")
        elif disallowed_fields:
            raise ValidationError(f"Invalid fields: {', '.join(disallowed_fields)}")

    @classmethod
    def is_post_request_valid(cls, request) -> None:
        """Ensure the requesting user can patch the provided fields."""
        requesting_user = request.user
        if not cls.is_admin(requesting_user):
            raise PermissionError("You do not have permission to create a user")

        request_data_keys = set(request.data)
        valid_fields = cls.get_fields(
            operation="post", table_name="user", permission_type=admin_global
        )
        disallowed_fields = request_data_keys - set(valid_fields)

        if not valid_fields:
            raise PermissionDenied(f"You do not have create privileges ")
        elif disallowed_fields:
            raise ValidationError(f"Invalid fields: {', '.join(disallowed_fields)}")
