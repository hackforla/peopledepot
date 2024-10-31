import inspect
import pytest
import sys
from unittest.mock import patch, mock_open
from rest_framework.exceptions import ValidationError, PermissionDenied
from core.api.permission_validation  import PermissionValidation
from core.api.user_request import UserRequest
from constants import admin_global, admin_project, member_project, practice_lead_project
from core.tests.utils.seed_constants import garry_name, wanda_admin_project, wally_name, zani_name, patti_name
from core.tests.utils.seed_user import SeedUser


keys = ["table_name", "field_name", "get", "patch", "post"]
rows = [
    ["user", "field1", member_project, practice_lead_project, admin_global],
    ["user", "field2", admin_project, admin_project, admin_global],
    ["user", "field3", admin_project, admin_global, admin_global],
    ["user", "system_field", member_project, "", ""],
    ["foo", "bar", member_project, member_project, member_project],
]
# Create an array of dictionaries with keys specified by keys[] andsss
# values for each row specified by rows
mock_data = [dict(zip(keys, row)) for row in rows]

class MockSimplifiedRequest():
    def __init__(self, user, data, method):
        self.user = user
        self.data = data
        self.method = method


@pytest.fixture
def mock_csv_data():
    """Fixture to provide mock CSV field permissions."""
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


# Beginner Tip:
# Mocking means creating a "fake" version of a function that behaves how you want for testing purposes.
# This allows us to test code without relying on external resources like databases.
@patch("builtins.open", new_callable=mock_open)
@patch("csv.DictReader")
def test_csv_field_permissions(mock_dict_reader, __mock_open__, mock_csv_data):
    """Test that get_csv_field_permissions returns the correct parsed data."""
    mock_dict_reader.return_value = mock_csv_data

    result = PermissionValidation.get_csv_field_permissions()
    assert result == mock_csv_data


@patch.object(PermissionValidation, "get_csv_field_permissions")
@pytest.mark.load_user_data_required  # see load_user_data_required in conftest.py
@pytest.mark.django_db
@pytest.mark.parametrize(
    "permission_type, operation, table_name, expected_results",
    [
        [member_project, "get", "user", {"field1", "system_field"}],
        [practice_lead_project, "get", "user", {"field1", "system_field"}],
        [admin_project, "get", "user", {"field1", "field2", "field3", "system_field"}],
        [admin_global, "get", "user", {"field1", "field2", "field3", "system_field"}],
        [member_project, "patch", "user", set()],
        [practice_lead_project, "patch", "user", {"field1"}],
        [admin_project, "patch", "user", {"field1", "field2"}],
        [admin_global, "patch", "user", {"field1", "field2", "field3"}],
        [member_project, "post", "user", set()],
        [practice_lead_project, "post", "user", set()],
        [admin_project, "post", "user", set()],
        [admin_global, "patch", "user", {"field1", "field2", "field3"}],
    ]
)
def test_role_field_permissions(get_csv_field_permissions, permission_type, operation, table_name, expected_results):

    # SETUP
    get_csv_field_permissions.return_value = mock_data
    valid_fields = PermissionValidation.get_fields(operation=operation, permission_type=permission_type, table_name=table_name)
    assert set(valid_fields) == expected_results

@pytest.mark.django_db
@pytest.mark.load_user_data_required  # see load_user_data_required in conftest.py
def test_is_admin():
    """Test that is_admin returns True for an admin user."""
    admin_user = SeedUser.get_user(garry_name)

    assert PermissionValidation.is_admin(admin_user) is True


@pytest.mark.django_db
@pytest.mark.load_user_data_required  # see load_user_data_required in conftest.py
def test_is_not_admin():
    """Test that is_admin returns True for an admin user."""
    admin_user = SeedUser.get_user(wanda_admin_project)
    assert PermissionValidation.is_admin(admin_user) is False


@pytest.mark.parametrize(
    "request_user_name, response_related_user_name, expected_permission_type",
    [
        # Wanda is an admin project for website, Wally is on the same project => admin_project
        (wanda_admin_project, wally_name, admin_project),
        # Wally is a project member for website, Wanda is on the same project => member_project
        (wally_name, wanda_admin_project, member_project),
        # Garry is both a project admin for website and a global admin => admin_global
        (garry_name, wally_name, admin_global),
        # Wally is a project member of website and Garry is a project lead on the same team
        # => member_project
        (wally_name, garry_name, member_project),
        # Garry is a global admin.  Even though Patti is not assigned to same team => admin_global
        (garry_name, patti_name, admin_global),
        # Patti has no project in common with Garry => ""
        (patti_name, wally_name, ""),
        # Zani is part of two projects with different permission types
        # Zani is a member_project for website, Wally is assigned same team => member_project
        (zani_name, wally_name, member_project),
        # Zani is a project admin for website, Wally is assigned same team => admin_project
        (zani_name, patti_name, admin_project),
  
    ],
)
@pytest.mark.django_db
@pytest.mark.load_user_data_required  # see load_user_data_required in conftest.py
def test_get_most_privileged_perm_type(
    request_user_name, response_related_user_name, expected_permission_type
):
    """Test that the correct permission type is returned."""
    request_user = SeedUser.get_user(request_user_name)
    response_related_user = SeedUser.get_user(response_related_user_name)
    assert (
        PermissionValidation.get_most_privileged_perm_type(
            request_user, response_related_user
        )
        == expected_permission_type
    )


@pytest.mark.django_db
@pytest.mark.load_user_data_required
@patch.object(PermissionValidation, "get_csv_field_permissions", return_value=mock_data)
def test_patch_with_valid_fields(__csv_field_permissions__):
    """Test that validate_user_fields_patchable does not raise an error for valid fields."""

    # Create a PATCH request with a JSON payload
    patch_data = {
        "field1": "foo",
        "field2": "bar"
    }
    mock_simplified_request = MockSimplifiedRequest (
        method = "PATCH",
        user = SeedUser.get_user(wanda_admin_project),
        data = patch_data
    )

    UserRequest.validate_fields(
        response_related_user=SeedUser.get_user(wally_name),
        request=mock_simplified_request,
    )
    assert True


@pytest.mark.django_db
@pytest.mark.load_user_data_required
@patch.object(PermissionValidation, "get_csv_field_permissions", return_value=mock_data)
def test_patch_with_invalid_fields(__csv_field_permissions__):
    """Test that validate_user_fields_patchable raises a ValidationError for invalid fields."""
    patch_data = {
        "field1": "foo",
        "field2": "bar",
        "field3": "not valid for patch"
    }
    mock_simplified_request = MockSimplifiedRequest (
        method = "PATCH",
        user = SeedUser.get_user(wanda_admin_project),
        data = patch_data
    )

    with pytest.raises(ValidationError):
        UserRequest.validate_fields(
            response_related_user=SeedUser.get_user(wally_name),
            request=mock_simplified_request,
    )       


@pytest.mark.django_db
@patch.object(PermissionValidation, "get_csv_field_permissions", return_value=mock_data)
def test_patch_fields_no_privileges(__csv_field_permissions__):
    """Test that validate_user_fields_patchable raises a PermissionError when no privileges exist."""
    patch_data = {"field1": "foo"}
    mock_simplified_request = MockSimplifiedRequest(
        method="PATCH", user=SeedUser.get_user(wally_name), data=patch_data
    )

    with pytest.raises(PermissionDenied):
        UserRequest.validate_fields(
            response_related_user=SeedUser.get_user(wally_name),
            request=mock_simplified_request,
        )


@pytest.mark.django_db
@pytest.mark.load_user_data_required
@patch.object(PermissionValidation, "get_csv_field_permissions", return_value=mock_data)
def test_post_with_valid_fields(__csv_field_permissions__):
    """Test that validate_user_fields_patchable does not raise an error for valid fields."""

    # Create a POST request with a JSON payload
    post_data = {"field1": "foo", "field2": "bar"}
    mock_simplified_request = MockSimplifiedRequest(
        method="POST", user=SeedUser.get_user(garry_name), data=post_data
    )

    UserRequest.validate_fields(
        request=mock_simplified_request,
    )
    assert True


@pytest.mark.django_db
@pytest.mark.load_user_data_required
@patch.object(PermissionValidation, "get_csv_field_permissions", return_value=mock_data)
def test_post_with_invalid_fields(__csv_field_permissions__):
    """Test that validate_user_fields_patchable raises a ValidationError for invalid fields."""
    post_data = {"field1": "foo", "field2": "bar", "system_field": "not valid for post"}
    mock_simplified_request = MockSimplifiedRequest(
        method="POST", user=SeedUser.get_user(garry_name), data=post_data
    )

    with pytest.raises(ValidationError):
        UserRequest.validate_fields(
            response_related_user=SeedUser.get_user(wally_name),
            request=mock_simplified_request,
        )


@pytest.mark.django_db
@patch.object(PermissionValidation, "get_csv_field_permissions", return_value=mock_data)
def test_patch_fields_no_privileges(__csv_field_permissions__):
    """Test that validate_user_fields_patchable raises a PermissionError when no privileges exist."""
    patch_data = {"field1": "foo"}
    mock_simplified_request = MockSimplifiedRequest(
        method="PATCH", user=SeedUser.get_user(wally_name), data=patch_data
    )

    with pytest.raises(PermissionDenied):
        UserRequest.validate_fields(
            response_related_user=SeedUser.get_user(wanda_admin_project),
            request=mock_simplified_request,
        )


# def test_clear_cache():
#     """Test that clear cache works by calling cache_clear on the cached methods."""
#     current_module = sys.modules[__name__]  # Get the current module
#     before_cached_count = len(inspect.getmembers(current_module, inspect.isfunction))
#     # assert before_cached_count > 0
#     FieldPermissionCheck.clear_all_caches()
#     after_cached_count = inspect.getmembers(current_module, inspect.isfunction)
#     assert after_cached_count == 0