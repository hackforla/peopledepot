from unittest.mock import mock_open
from unittest.mock import patch

import pytest
from rest_framework.exceptions import PermissionDenied
from rest_framework.exceptions import ValidationError

from constants import ADMIN_GLOBAL
from constants import ADMIN_PROJECT
from constants import MEMBER_PROJECT
from constants import PRACTICE_LEAD_PROJECT
from core.api.access_control import AccessControl
# from core.api.user_related_request import UserRelatedRequest
from core.api.views import UserViewSet
from test_data.utils.seed_constants import garry_name
from test_data.utils.seed_constants import patti_name
from test_data.utils.seed_constants import wally_name
from test_data.utils.seed_constants import wanda_admin_project
from test_data.utils.seed_constants import zani_name
from test_data.utils.seed_user import SeedUser

keys = ["table_name", "field_name", "get", "patch", "post"]
rows = [
    ["User", "field1", MEMBER_PROJECT, PRACTICE_LEAD_PROJECT, ADMIN_GLOBAL],
    ["User", "field2", ADMIN_PROJECT, ADMIN_PROJECT, ADMIN_GLOBAL],
    ["User", "field3", ADMIN_PROJECT, ADMIN_GLOBAL, ADMIN_GLOBAL],
    ["User", "system_field", MEMBER_PROJECT, "", ""],
    ["foo", "bar", MEMBER_PROJECT, MEMBER_PROJECT, MEMBER_PROJECT],
]
# Create an array of dictionaries with keys specified by keys[] andsss
# values for each row specified by rows
mock_data = [dict(zip(keys, row)) for row in rows]


class MockSimplifiedRequest:
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
            "field_name": "gmail_email",
            "view": "viewer",
            "update": "moderator",
            "create": ADMIN_GLOBAL,
        },
        {
            "operation": "create",
            "table_name": "user",
            "field_name": "name",
            "view": "viewer",
            "update": "moderator",
            "create": ADMIN_GLOBAL,
        },
    ]


@pytest.mark.django_db
def test_is_admin():
    """Test that is_admin returns True for an admin user."""
    admin_user = SeedUser.get_user(garry_name)

    assert AccessControl.is_admin(admin_user) is True


@pytest.mark.django_db
def test_is_not_admin():
    """Test that is_admin returns True for an admin user."""
    admin_user = SeedUser.get_user(wanda_admin_project)
    assert AccessControl.is_admin(admin_user) is False


@pytest.mark.parametrize(  # noqa: PT006 PT007
    "request_user_name, response_related_user_name, expected_permission_type",
    (
        # Wanda is an admin project for website, Wally is on the same project => ADMIN_PROJECT
        (wanda_admin_project, wally_name, ADMIN_PROJECT),
        # Wally is a project member for website, Wanda is on the same project => MEMBER_PROJECT
        (wally_name, wanda_admin_project, MEMBER_PROJECT),
        # Garry is both a project admin for website and a global admin => ADMIN_GLOBAL
        (garry_name, wally_name, ADMIN_GLOBAL),
        # Wally is a project member of website and Garry is a project lead on the same team
        # => MEMBER_PROJECT
        (wally_name, garry_name, MEMBER_PROJECT),
        # Garry is a global admin.  Even though Patti is not assigned to same team => ADMIN_GLOBAL
        (garry_name, patti_name, ADMIN_GLOBAL),
        # Patti has no project in common with Garry => ""
        (patti_name, wally_name, ""),
        # Zani is part of two projects with different permission types
        # Zani is a MEMBER_PROJECT for website, Wally is assigned same team => MEMBER_PROJECT
        (zani_name, wally_name, MEMBER_PROJECT),
        # Zani is a project admin for website, Wally is assigned same team => ADMIN_PROJECT
        (zani_name, patti_name, ADMIN_PROJECT),
    ),
)
@pytest.mark.django_db
# see load_user_data_required in conftest.py
def test_get_highest_shared_project_perm_type(
    request_user_name, response_related_user_name, expected_permission_type
):
    """Test that the correct permission type is returned."""
    request_user = SeedUser.get_user(request_user_name)
    response_related_user = SeedUser.get_user(response_related_user_name)
    assert (
        AccessControl.get_highest_shared_project_perm_type(request_user, response_related_user)
        == expected_permission_type
    )
