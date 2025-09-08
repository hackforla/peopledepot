from unittest.mock import mock_open, patch

import pytest
from rest_framework.exceptions import PermissionDenied, ValidationError

from constants import admin_global, admin_project, member_project, practice_lead_project
from core.api.permission_validation import PermissionValidation
from core.api.user_related_request import UserRelatedRequest
from core.api.views import UserViewSet
from core.tests.utils.seed_constants import (
    garry_name, patti_name, wally_name, wanda_admin_project, zani_name
)
from core.tests.utils.seed_user import SeedUser

# Mock CSV field permission data
keys = ["table_name", "field_name", "get", "patch", "post"]
rows = [
    ["User", "field1", member_project, practice_lead_project, admin_global],
    ["User", "field2", admin_project, admin_project, admin_global],
    ["User", "field3", admin_project, admin_global, admin_global],
    ["User", "system_field", member_project, "", ""],
    ["foo", "bar", member_project, member_project, member_project],
]
mock_data = [dict(zip(keys, row)) for row in rows]


class MockSimplifiedRequest:
    """
    A simplified mock request object for testing PATCH and POST validation.

    Attributes:
        user: The user making the request.
        data (dict): The request payload.
        method (str): The HTTP method of the request.
    """

    def __init__(self, user, data, method):
        self.user = user
        self.data = data
        self.method = method


@pytest.fixture
def mock_csv_data():
    """
    Fixture that returns example CSV field permissions.

    Returns:
        list[dict]: A list of dictionaries simulating CSV rows of field permissions.
    """
    return [
        {
            "operation": "update",
            "table_name": "user",
            "field_name": "email",
            "view": "viewer",
            "update": "moderator",
            "create": admin_global,
        },
        {
            "operation": "create",
            "table_name": "user",
            "field_name": "name",
            "view": "viewer",
            "update": "moderator",
            "create": admin_global,
        },
    ]


@patch("builtins.open", new_callable=mock_open)
@patch("csv.DictReader")
def test_csv_field_permissions(mock_dict_reader, _, mock_csv_data):
    """
    Test that CSV field permissions are correctly parsed.

    Args:
        mock_dict_reader: Mocked CSV.DictReader.
        _: Mocked open function (unused).
        mock_csv_data: Fixture providing expected CSV data.
    """
    mock_dict_reader.return_value = mock_csv_data
    result = PermissionValidation.get_csv_field_permissions()
    assert result == mock_csv_data


@pytest.mark.django_db
@pytest.mark.load_user_data_required
def test_is_admin():
    """Verify that is_admin returns True for a global or project admin user."""
    admin_user = SeedUser.get_user(garry_name)
    assert PermissionValidation.is_admin(admin_user) is True


@pytest.mark.django_db
@pytest.mark.load_user_data_required
def test_is_not_admin():
    """Verify that is_admin returns False for a non-admin user."""
    non_admin_user = SeedUser.get_user(wanda_admin_project)
    assert PermissionValidation.is_admin(non_admin_user) is False


@pytest.mark.parametrize(
    "request_user_name, response_related_user_name, expected_permission_type",
    (
        (wanda_admin_project, wally_name, admin_project),
        (wally_name, wanda_admin_project, member_project),
        (garry_name, wally_name, admin_global),
        (wally_name, garry_name, member_project),
        (garry_name, patti_name, admin_global),
        (patti_name, wally_name, ""),
        (zani_name, wally_name, member_project),
        (zani_name, patti_name, admin_project),
    ),
)
@pytest.mark.django_db
@pytest.mark.load_user_data_required
def test_get_most_privileged_perm_type(
    request_user_name, response_related_user_name, expected_permission_type
):
    """
    Verify that get_most_privileged_perm_type returns the correct permission type.

    Args:
        request_user_name: The name of the user making the request.
        response_related_user_name: The name of the user being checked.
        expected_permission_type: The expected permission type string.
    """
    request_user = SeedUser.get_user(request_user_name)
    response_related_user = SeedUser.get_user(response_related_user_name)
    result = PermissionValidation.get_most_privileged_perm_type(request_user, response_related_user)
    assert result == expected_permission_type


@pytest.mark.django_db
@pytest.mark.load_user_data_required
@patch.object(PermissionValidation, "get_csv_field_permissions", return_value=mock_data)
def test_patch_with_valid_fields(_):
    """
    Verify that validate_patch_fields succeeds for a PATCH request with allowed fields.
    """
    patch_data = {"field1": "foo", "field2": "bar"}
    mock_request = MockSimplifiedRequest(
        method="PATCH",
        user=SeedUser.get_user(wanda_admin_project),
        data=patch_data,
    )
    UserRelatedRequest.validate_patch_fields(
        view=UserViewSet, obj=SeedUser.get_user(wally_name), request=mock_request
    )
    assert True


@pytest.mark.django_db
@pytest.mark.load_user_data_required
@patch.object(PermissionValidation, "get_csv_field_permissions", return_value=mock_data)
def test_patch_with_invalid_fields(_):
    """
    Verify that validate_patch_fields raises ValidationError when PATCH contains invalid fields.
    """
    patch_data = {"field1": "foo", "field2": "bar", "field3": "not valid for patch"}
    mock_request = MockSimplifiedRequest(
        method="PATCH",
        user=SeedUser.get_user(wanda_admin_project),
        data=patch_data,
    )
    with pytest.raises(ValidationError):
        UserRelatedRequest.validate_patch_fields(
            view=UserViewSet, obj=SeedUser.get_user(wanda_admin_project), request=mock_request
        )


@pytest.mark.django_db
@patch.object(PermissionValidation, "get_csv_field_permissions", return_value=mock_data)
def test_patch_fields_no_privileges(_):
    """
    Verify that validate_patch_fields raises PermissionDenied when user has no privilege.
    """
    patch_data = {"field1": "foo"}
    mock_request = MockSimplifiedRequest(
        method="PATCH", user=SeedUser.get_user(wally_name), data=patch_data
    )
    with pytest.raises(PermissionDenied):
        UserRelatedRequest.validate_patch_fields(
            view=UserViewSet, obj=SeedUser.get_user(wally_name), request=mock_request
        )


@pytest.mark.django_db
@pytest.mark.load_user_data_required
@patch.object(PermissionValidation, "get_csv_field_permissions", return_value=mock_data)
def test_post_with_valid_fields(_):
    """
    Verify that validate_post_fields succeeds for a POST request with allowed fields.
    """
    post_data = {"field1": "foo", "field2": "bar"}
    mock_request = MockSimplifiedRequest(
        method="POST", user=SeedUser.get_user(garry_name), data=post_data
    )
    UserRelatedRequest.validate_post_fields(request=mock_request, view=UserViewSet)
    assert True


@pytest.mark.django_db
@pytest.mark.load_user_data_required
@patch.object(PermissionValidation, "get_csv_field_permissions", return_value=mock_data)
def test_post_with_invalid_fields(_):
    """
    Verify that validate_post_fields raises ValidationError when POST contains invalid fields.
    """
    post_data = {"field1": "foo", "field2": "bar", "system_field": "not valid for post"}
    mock_request = MockSimplifiedRequest(
        method="POST", user=SeedUser.get_user(garry_name), data=post_data
    )
    with pytest.raises(ValidationError):
        UserRelatedRequest.validate_post_fields(request=mock_request, view=UserViewSet)
