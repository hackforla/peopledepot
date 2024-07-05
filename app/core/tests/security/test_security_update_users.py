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

from core.models import User
from core.permission_util import PermissionUtil
from core.tests.utils.seed_constants import garry_name
from core.tests.utils.seed_constants import patrick_name
from core.tests.utils.seed_constants import patti_name
from core.tests.utils.seed_constants import valerie_name
from core.tests.utils.seed_constants import wally_name
from core.tests.utils.seed_constants import wanda_name
from core.tests.utils.seed_constants import winona_name
from core.tests.utils.seed_constants import zani_name
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

    def test_admin_update_request_succeeds(self):  #
        requester = SeedUser.get_user(garry_name)
        client = APIClient()
        client.force_authenticate(user=requester)

        target_user = SeedUser.get_user(valerie_name)
        url = reverse("user-detail", args=[target_user.uuid])
        data = {
            "last_name": "Updated",
            "gmail": "update@example.com",
        }
        response = client.patch(url, data, format="json")
        assert response.status_code == status.HTTP_200_OK
    
    def test_admin_cannot_update_created_at(self):
        requester = SeedUser.get_user(garry_name)
        client = APIClient()
        client.force_authenticate(user=requester)

        target_user = SeedUser.get_user(valerie_name)
        url = reverse("user-detail", args=[target_user.uuid])
        data = {
            "created_at": "2022-01-01T00:00:00Z",
        }
        response = client.patch(url, data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "created_at" in response.json()[0]

    def test_is_update_request_valid(self):
        logged_in_user, response = self.authenticate_user(
            SeedUser.get_user(garry_name).first_name
        )
        assert logged_in_user is not None
        assert response.status_code == status.HTTP_200_OK
        
    def validate_fields_updateable(self):
        PermissionUtil.validate_fields_updateable(
            SeedUser.get_user(garry_name),
            SeedUser.get_user(valerie_name),
            ["first_name", "last_name", "gmail"],
        )

    def test_created_at_not_updateable(self):
        with pytest.raises(Exception):
            PermissionUtil.validate_fields_updateable(
                SeedUser.get_user(garry_name),
                SeedUser.get_user(valerie_name),
                ["created_at"],
            )
    def test_project_lead_can_update_name(self):
        PermissionUtil.validate_fields_updateable(
            SeedUser.get_user(wanda_name),
            SeedUser.get_user(wally_name),
            ["first_name", "last_name"],
        )

    def test_project_lead_cannot_update_current_title(self):
        with pytest.raises(Exception):
            PermissionUtil.validate_fields_updateable(
                SeedUser.get_user(wanda_name),
                SeedUser.get_user(wally_name),
                ["current_title"],
            )

    def test_cannot_update_first_name_for_member_of_other_project(self):
        with pytest.raises(Exception):
            PermissionUtil.validate_fields_updateable(
                SeedUser.get_user(wanda_name),
                SeedUser.get_user(patti_name),
                ["first_name"],
            )

    def test_team_member_cannot_update_first_name_for_member_of_same_project(self):
        with pytest.raises(Exception):
            PermissionUtil.validate_fields_updateable(
                SeedUser.get_user(wally_name),
                SeedUser.get_user(winona_name),
                ["first_name"],
            )
 
    def test_multi_project_requester_can_update_first_name_of_member_if_requester_is_project_leader(self):
        PermissionUtil.validate_fields_updateable(
            SeedUser.get_user(zani_name), SeedUser.get_user(wally_name), ["first_name"]
        )

    def test_multi_project_user_cannot_update_first_name_of_member_if_reqiester_is_project_member(self):
        with pytest.raises(Exception):
            PermissionUtil.validate_fields_updateable(
                SeedUser.get_user(zani_name),
                SeedUser.get_user(patti_name),
                ["first_name"],
            )
