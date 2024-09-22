import pytest
from rest_framework.exceptions import ValidationError

from core.field_permissions import FieldPermissions
from core.permission_util import PermissionUtil
from core.tests.utils.seed_constants import garry_name
from core.tests.utils.seed_constants import patti_name
from core.tests.utils.seed_constants import valerie_name
from core.tests.utils.seed_constants import wally_name
from core.tests.utils.seed_constants import wanda_admin_project
from core.tests.utils.seed_constants import winona_name
from core.tests.utils.seed_constants import zani_name
from core.tests.utils.seed_user import SeedUser

count_website_members = 4
count_people_depot_members = 3
count_members_either = 6


def fields_match(first_name, user_data, fields):
    for user in user_data:
        if user["first_name"] == first_name:
            return set(user.keys()) == set(fields)
    return False


@pytest.mark.django_db
class TestValidateFieldsPatchable:
    # Some tests change FieldPermission attribute values.
    # derive_cru resets the values before each test - otherwise
    # the tests would interfere with each other
    def setup_method(self):
        FieldPermissions.derive_cru_fields()

    # Some tests change FieldPermission attribute values.
    # derive_cru resets the values after each test
    # Redundant with setup_method, but good practice
    def teardown_method(self):
        FieldPermissions.derive_cru_fields()

    def test_created_at_not_updateable(self):
        """Test validate_fields_patchable raises ValidationError
        if requesting fields include created_at.
        """
        with pytest.raises(ValidationError):
            PermissionUtil.validate_fields_patchable(
                SeedUser.get_user(garry_name),
                SeedUser.get_user(valerie_name),
                ["created_at"],
            )

    def test_admin_project_can_patch_name(self):
        """Test validate_fields_patchable succeeds
        if requesting fields include first_name and last_name **WHEN**
        the requester is a project lead.
        """
        PermissionUtil.validate_fields_patchable(
            SeedUser.get_user(wanda_admin_project),
            SeedUser.get_user(wally_name),
            ["first_name", "last_name"],
        )

    def test_admin_project_cannot_patch_current_title(self):
        """Test validate_fields_patchable raises ValidationError
        if requesting fields include current_title **WHEN** requester
        is a project lead.
        """
        with pytest.raises(ValidationError):
            PermissionUtil.validate_fields_patchable(
                SeedUser.get_user(wanda_admin_project),
                SeedUser.get_user(wally_name),
                ["current_title"],
            )

    def test_cannot_patch_first_name_for_member_of_other_project(self):
        """Test validate_fields_patchable raises ValidationError
        if requesting fields include first_name **WHEN** requester
        is a member of a different project.
        """
        with pytest.raises(PermissionError):
            PermissionUtil.validate_fields_patchable(
                SeedUser.get_user(wanda_admin_project),
                SeedUser.get_user(patti_name),
                ["first_name"],
            )

    def test_team_member_cannot_patch_first_name_for_member_of_same_project(self):
        """Test validate_fields_patchable raises ValidationError
        **WHEN** requester is only a project team member.
        """
        with pytest.raises(PermissionError):
            PermissionUtil.validate_fields_patchable(
                SeedUser.get_user(wally_name),
                SeedUser.get_user(winona_name),
                ["first_name"],
            )

    def test_multi_project_requester_can_patch_first_name_of_member_if_requester_is_admin_projecter(
        self,
    ):
        """Test validate_fields_patchable succeeds for first name
        **WHEN** requester assigned to multiple projects
        is a project lead for the user being patched.
        """
        PermissionUtil.validate_fields_patchable(
            SeedUser.get_user(zani_name), SeedUser.get_user(patti_name), ["first_name"]
        )

    def test_multi_project_user_cannot_patch_first_name_of_member_if_requester_is_member_project(
        self,
    ):
        """Test validate_fields_patchable raises ValidationError
        **WHEN** requester assigned to multiple projects
        is only a project team member for the user being patched.
        """
        with pytest.raises(PermissionError):
            PermissionUtil.validate_fields_patchable(
                SeedUser.get_user(zani_name),
                SeedUser.get_user(wally_name),
                ["first_name"],
            )
