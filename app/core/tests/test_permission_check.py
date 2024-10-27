import pytest
from unittest.mock import patch, MagicMock, mock_open
from rest_framework.exceptions import ValidationError, PermissionDenied
from core.api.permission_check  import FieldPermissionCheck
from constants import admin_global, admin_project, member_project, practice_lead_project
from core.tests.utils.seed_constants import garry_name, wanda_admin_project, wally_name, zani_name, patti_name
from core.tests.utils.seed_user import SeedUser



# @pytest.fixture
# def mock_permissions():
#     """Fixture to provide mock permission types."""
#     return [
#         {"name": admin_global, "rank": 1},
#         {"name": "moderator", "rank": 2},
#         {"name": "viewer", "rank": 3},
#     ]


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


def mock_csv_data2():
    """Fixture to provide mock CSV field permissions."""
    keys = ["table_name", "field_name", "view", "update", "create"]
    rows = [
        ["user", "field1", member_project, admin_project, admin_global],
        ["user", "field2", admin_project, admin_project, admin_global],
        ["user", "field3", admin_project, admin_global, admin_global],
        ["foo", "field1", member_project, member_project, member_project],
    ]
    # Create an array of dictionaries with keys specified by keys[] and
    # values for each row specified by rows
    return [dict(zip(keys, row)) for row in rows]


# Beginner Tip:
# Mocking means creating a "fake" version of a function that behaves how you want for testing purposes.
# This allows us to test code without relying on external resources like databases.

# @patch("core.models.PermissionType.objects.values")  
# def test_get_rank_dict(mock_for_values_call):  
#     """Test that get_rank_dict returns the correct data."""
    
#     # PermissionType.objects.values() is called from get_rank_dict
#     # This is mocked by @patch to avoid calling the db and to isolate the test
#     # The return value will be the value specified below
#     mock_for_values_call.return_value = [
#         {"name": admin_global, "rank": 1},
#         {"name": "moderator", "rank": 2},
#         {"name": "viewer", "rank": 3},
#     ]

#     result = FieldPermissionCheck.get_rank_dict()
#     expected_result = {
#         admin_global: 1,
#         "moderator": 2,
#         "viewer": 3,
#     }

#     assert result == expected_result


@patch("builtins.open", new_callable=mock_open)
@patch("csv.DictReader")
@pytest.mark.skip
def test_csv_field_permissions(mock_dict_reader, __mock_open__, mock_csv_data):
    """Test that csv_field_permissions returns the correct parsed data."""
    mock_dict_reader.return_value = mock_csv_data

    result = FieldPermissionCheck.csv_field_permissions()
    assert result == mock_csv_data


@patch.object(FieldPermissionCheck, "csv_field_permissions")
@pytest.mark.load_user_data_required  # see load_user_data_required in conftest.py
@pytest.mark.django_db
@pytest.mark.parametrize(
    "permission_type, operation, table, expected_results",
    [
        [member_project, "read", "user", {"field1", "system_field"}],
        [practice_lead_project, "read", "user", {"field1", "system_field"}],
        [admin_project, "read", "user", {"field1", "field2", "field3", "system_field"}],
        [admin_global, "read", "user", {"field1", "field2", "field3", "system_field"}],
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
def test_role_field_permissions(csv_field_permissions, permission_type, operation, table, expected_results):

    # SETUP

    keys = ["table_name", "field_name", "read", "patch", "post"]
    rows = [
        ["user", "field1", member_project, practice_lead_project, admin_global],
        ["user", "field2", admin_project, admin_project, admin_global],
        ["user", "field3", admin_project, admin_global, admin_global],
        ["user", "system_field", member_project, "", ""],
        ["foo", "bar", member_project, member_project, member_project],
    ]
    # Create an array of dictionaries with keys specified by keys[] and
    # values for each row specified by rows
    mock_data = [dict(zip(keys, row)) for row in rows]
    csv_field_permissions.return_value = mock_data
    valid_fields = FieldPermissionCheck.role_field_permissions(operation=operation, permission_type=permission_type, table_name=table)
    assert set(valid_fields) == expected_results

@pytest.mark.django_db
@pytest.mark.load_user_data_required  # see load_user_data_required in conftest.py
def test_is_admin():
    """Test that is_admin returns True for an admin user."""
    admin_user = SeedUser.get_user(garry_name)

    assert FieldPermissionCheck.is_admin(admin_user) is True


@pytest.mark.django_db
@pytest.mark.load_user_data_required  # see load_user_data_required in conftest.py
def test_is_not_admin():
    """Test that is_admin returns True for an admin user."""
    admin_user = SeedUser.get_user(wanda_admin_project)
    assert FieldPermissionCheck.is_admin(admin_user) is False


@pytest.mark.parametrize(
    "request_user_name, target_user_name, expected_permission_type",
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
    request_user_name, target_user_name, expected_permission_type
):
    """Test that the correct permission type is returned."""
    request_user = SeedUser.get_user(request_user_name)
    target_user = SeedUser.get_user(target_user_name)
    assert (
        FieldPermissionCheck.get_most_privileged_perm_type(
            request_user, target_user
        )
        == expected_permission_type
    )


# @patch.object(FieldPermissionCheck, "get_rank_dict", return_value={ admin_global: 1, admin_project: 2, practice_lead_project: 3})
# @patch.object(FieldPermissionCheck, "csv_field_permissions", return_value = \
#     { "table_name", "user", "operation": "update",  "field_name": "field1", "create": admin_project, ""
# }
@pytest.mark.django_db
@pytest.mark.skip
@patch.object(FieldPermissionCheck, "role_field_permissions", return_value=["email"])
def test_validate_user_fields_patchable_valid(mock_role_permissions):
    """Test that validate_user_fields_patchable does not raise an error for valid fields."""
    try:
        FieldPermissionCheck.validate_user_fields_patchable(
            MagicMock(), MagicMock(), ["email"]
        )
    except ValidationError:
        pytest.fail("ValidationError was raised unexpectedly!")


@pytest.mark.django_db
@pytest.mark.skip
@patch.object(FieldPermissionCheck, "role_field_permissions", return_value=["email"])
@patch.object(
    FieldPermissionCheck, "get_most_privileged_perm_type", return_value=["dummy"]
)
def test_validate_user_fields_patchable_invalid(mock_role_permissions):
    """Test that validate_user_fields_patchable raises a ValidationError for invalid fields."""
    with pytest.raises(ValidationError, match="Invalid fields: name"):
        FieldPermissionCheck.validate_user_fields_patchable(
            MagicMock(), MagicMock(), ["name"]
        )


@pytest.mark.django_db
@pytest.mark.skip
@patch.object(FieldPermissionCheck, "role_field_permissions", return_value=[])
def test_validate_user_fields_patchable_no_privileges(mock_role_permissions):
    """Test that validate_user_fields_patchable raises a PermissionError when no privileges exist."""
    with pytest.raises(PermissionError, match="You do not have update privileges"):
        FieldPermissionCheck.validate_user_fields_patchable(
            MagicMock(), MagicMock(), ["email"]
        )


def test_clear_cache():
    """Test that clear cache works by calling cache_clear on the cached methods."""
    with patch.object(
        FieldPermissionCheck.csv_field_permissions, "cache_clear"
    ) as mock_csv_clear, patch.object(
        FieldPermissionCheck.get_rank_dict, "cache_clear"
    ) as mock_rank_clear:
        FieldPermissionCheck.clear()
        mock_csv_clear.assert_called_once()
        mock_rank_clear.assert_called_once()
