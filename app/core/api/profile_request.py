import csv
from constants import profile_permissions_csv_file
from rest_framework.exceptions import ValidationError, PermissionDenied, MethodNotAllowed
from core.api.permission_validation import PermissionValidation
from typing import Any, Dict, List

class ProfileRequest:
    def get_csv_field_permissions() -> Dict[str, Dict[str, List[Dict[str, Any]]]]:
        """Read the field permissions from a CSV file."""
        with open(profile_permissions_csv_file, mode="r", newline="") as file:
            reader = csv.DictReader(file)
            return list(reader)

    @classmethod
    def get_fields(
        cls, table_name: str, operation: str) -> List[str]:
        """Return the valid fields for the given permission type."""

        valid_fields = []
        for field in cls.get_csv_field_permissions():
            if field["table_name"]==table_name and field[operation].upper()=="TRUE":
                valid_fields += [field["field_name"]]
        return valid_fields

    @classmethod
    def get_valid_patch_fields(cls):
        fields = cls.get_fields(
            operation="patch", table_name="user"
        )
        return fields

    @classmethod
    def get_read_fields(cls):
        fields = cls.get_fields(
            operation="get", table_name="user"
        )
        return fields

    @classmethod
    def validate_patch_request(cls, request) -> None:
        """Ensure the requesting user can patch the provided fields."""
        valid_fields = []
        valid_fields = cls.get_fields(
                table_name="user",
                operation="patch"
            )
        request_data_keys = set(request.data)
        disallowed_fields = request_data_keys - set(valid_fields)

        if not valid_fields:
            raise PermissionDenied(f"You do not have privileges ")
        elif disallowed_fields:
            raise ValidationError(f"Invalid fields: {', '.join(disallowed_fields)}")
