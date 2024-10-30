import csv
# import inspect
# import sys
# from functools import lru_cache
from constants import profile_value
from typing import Any, Dict, List
from rest_framework.exceptions import ValidationError, PermissionDenied, MethodNotAllowed
from constants import field_permissions_csv_file, admin_global  # Assuming you have this constant
from core.models import PermissionType, UserPermission

class ProfilePermissionCheck:

    @classmethod
    def get_fields_for_patch_request(cls):
        fields = cls.get_fields(
            operation="patch", table_name="user", permission_type=profile_value
        )
        return fields

    @classmethod
    def get_read_fields(cls):
        fields = cls.get_fields(
            operation="read", table_name="user", permission_type=profile_value
        )
        return fields

    @classmethod
    def validate_patch_request(cls, request) -> None:
        """Ensure the requesting user can patch the provided fields."""
        valid_fields = []
        if request.method == "POST":
            raise MethodNotAllowed("POST is not allowed for the me/profile API")
        elif request.method == "PATCH":
            valid_fields = cls.get_fields_for_profile_patch_request(
                table_name="user",
                request=request,
            )
        else:
            raise MethodNotAllowed("Not valid for REST method", request.method)
        request_data_keys = set(request.data)
        disallowed_fields = request_data_keys - set(valid_fields)

        if not valid_fields:
            raise PermissionDenied(f"You do not have privileges ")
        elif disallowed_fields:
            raise ValidationError(f"Invalid fields: {', '.join(disallowed_fields)}")
