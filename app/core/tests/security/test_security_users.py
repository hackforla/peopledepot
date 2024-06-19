# Change fields that can be viewed in code to what Bonnie specified
# Add update api test
# Write API to get token
# Create a demo script for adding users with password of Hello2024.
# Create a shell script for doing a get
# Create a shell script for doing a patch
# Change fields that can be viewed in my wiki to what Bonnie specified
# Add more tests for update
# Add print statements to explain what is being tested
# Add tests for the patch API
# Add tests for and implement put (disallow), post, and delete API
# Update my Wiki for put, patch, post, delete
# Add proposals:
#   - use flag instead of role for admin and verified
# . -
import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from core.constants import FieldPermissions
from core.constants import Fields
from core.constants import PermissionValue
from core.permission_util import PermissionUtil
from core.tests.utils.seed_data import Seed
from core.tests.utils.seed_user import SeedUser
from core.tests.utils.utils_test import show_test_info

count_website_members = 4
count_people_depot_members = 3
count_members_either = 6


def fields_match(first_name, user_data, fields):
    for user in user_data:
        if user["first_name"] == first_name:
            return set(user.keys()) == set(fields)
    return False


@pytest.mark.django_db
class TestUser:
    @classmethod
    def authenticate_user(cls, user_name):
        logged_in_user = SeedUser.get_user(user_name)
        client = APIClient()
        client.force_authenticate(user=logged_in_user)
        url = reverse("user-list")  # Update this to your actual URL name
        response = client.get(url)
        return logged_in_user, response

    def test_is_update_request_valid(self, user_tests_init):
        logged_in_user, response = self.authenticate_user(Seed.garry.first_name)
        assert logged_in_user is not None
        assert response.status_code == 200
        assert get_user_model().objects.count() > 0
        show_test_info("")
        show_test_info("==== Validating is_fields_valid function ====")
        show_test_info("")
        show_test_info("==> Validating global admin")
        show_test_info("")
        show_test_info(
            f"global admin will succeed for first name, last name, and email"
        )
        PermissionUtil.validate_update_request(
            Seed.garry.user, Seed.valerie.user, ["first_name", "last_name", "email"]
        )
        show_test_info(f"global admin will raise exception for created_at")
        with pytest.raises(Exception):
            PermissionUtil.validate_update_request(
                Seed.garry.user, Seed.valerie.user, ["created_at"]
            )
        show_test_info("")
        show_test_info("==> Validating project admin")
        show_test_info(
            f"project admin will succeed for first name, last name, and email with a project member"
        )
        PermissionUtil.validate_update_request(
            Seed.wanda.user, Seed.wally.user, ["first_name", "last_name"]
        )
        show_test_info(
            f"project admin will  raise exception for current title / project member combo"
        )
        with pytest.raises(Exception):
            PermissionUtil.validate_update_request(
                Seed.wanda.user, Seed.wally.user, ["current_title"]
            )
        show_test_info(
            f"project admin will raise exception for first name (or any field) / non-project member combo"
        )
        with pytest.raises(Exception):
            PermissionUtil.validate_update_request(
                Seed.wanda.user, Seed.patti.user, ["first_name"]
            )
        show_test_info("")
        show_test_info("=== Validating project member ===")
        show_test_info(
            "Validate project member cannot update first name of another project member"
        )
        with pytest.raises(Exception):
            PermissionUtil.validate_update_request(
                Seed.wally.user, Seed.winona.user, ["first_name"]
            )
        show_test_info(
            "==> Validating combo user with both project admin and project member roles"
        )
        show_test_info(
            "Validate combo user can update first name of a project member for which they are a project admin"
        )
        PermissionUtil.validate_update_request(
            Seed.zani.user, Seed.wally.user, ["first_name"]
        )
        show_test_info(
            "Validate combo user cannot update first name of a project member for which they are not a project admin"
        )
        with pytest.raises(Exception):
            PermissionUtil.validate_update_request(
                Seed.zani.user, Seed.patti.user, ["first_name"]
            )

    def test_can_read_logic(self, user_tests_init):
        show_test_info("=== Validating logic for can read===")
        show_test_info("==> is admin")
        show_test_info(
            "Validate is_admin returns true for a global admin and false for a project admin"
        )
        assert PermissionUtil.is_admin(Seed.garry.user)
        assert not PermissionUtil.is_admin(Seed.wanda.user)

        show_test_info("Globan admin can read senstive fields of any user")
        assert PermissionUtil.can_read_all_user(Seed.garry.user, Seed.valerie.user)

        show_test_info("==> project member")
        show_test_info("Project member can read basic info for another project member")
        assert PermissionUtil.can_read_basic_user(Seed.wally.user, Seed.winona.user)
        show_test_info("Team member can read basic info for another project member")
        assert PermissionUtil.can_read_basic_user(Seed.wally.user, Seed.wanda.user)
        show_test_info("Team member can read basic info for another project member")
        assert not PermissionUtil.can_read_basic_user(Seed.wally.user, Seed.garry.user)
        assert not PermissionUtil.can_read_all_user(Seed.wally.user, Seed.wanda.user)

        show_test_info("==> project admin")
        assert PermissionUtil.can_read_user_secure(Seed.wanda.user, Seed.wally.user)

    def test_global_admin(self, user_tests_init):
        logged_in_user, response = self.authenticate_user(Seed.garry.first_name)
        assert logged_in_user is not None
        assert response.status_code == 200
        assert get_user_model().objects.count() > 0
        assert len(response.json()) == len(SeedUser.users)

    def test_multi_project_user(self, user_tests_init):
        logged_in_user, response = self.authenticate_user(Seed.zani.first_name)
        assert logged_in_user is not None
        assert response.status_code == 200
        assert len(response.json()) == count_members_either
        assert fields_match(
            Seed.wanda.first_name,
            response.json(),
            FieldPermissions.read_fields["user"][PermissionValue.global_admin],
        )
        assert fields_match(
            Seed.patrick.first_name,
            response.json(),
            FieldPermissions.read_fields["user"][PermissionValue.basic],
        )

    def test_project_admin(self, user_tests_init):
        logged_in_user, response = self.authenticate_user(Seed.wanda.first_name)
        assert logged_in_user is not None
        assert response.status_code == 200
        assert len(response.json()) == count_website_members
        assert fields_match(
            Seed.winona.first_name,
            response.json(),
            Fields.read["user"][PermissionValue.global_admin],
        )

    def test_project_team_member(self, user_tests_init):
        logged_in_user, response = self.authenticate_user(Seed.wally.first_name)
        assert logged_in_user is not None
        assert response.status_code == 200
        assert fields_match(
            Seed.winona.first_name,
            response.json(),
            Fields.read["user"][PermissionValue.basic],
        )
        assert fields_match(
            Seed.wanda.first_name,
            response.json(),
            Fields.read["user"][PermissionValue.basic],
        )
        assert len(response.json()) == count_website_members

    def test_no_project(self, user_tests_init):
        logged_in_user, response = self.authenticate_user(Seed.valerie.first_name)
        assert logged_in_user is not None
        assert response.status_code == 200
        assert len(response.json()) == 0
