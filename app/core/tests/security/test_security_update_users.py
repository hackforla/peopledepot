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
from core.tests.utils.seed_constants import valerie_name
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

    def test_admin_update_api(self, load_test_user_data):  #
        show_test_info("==> Testing update global admin")
        show_test_info("Global admin can update last name and gmail field using API")
        user = SeedUser.get_user(valerie_name)
        url = reverse("user-detail", args=[user.uuid])
        data = {
            "last_name": "Updated",
            "gmail": "update@example.com",
        }
        client = APIClient()
        client.force_authenticate(user=SeedUser.get_user(garry_name))
        response = client.patch(url, data, format="json")
        assert response.status_code == status.HTTP_200_OK

        show_test_info("Global admin cannot update created_at")
        url = reverse("user-detail", args=[user.uuid])
        data = {
            "created_at": "2022-01-01T00:00:00Z",
        }
        response = client.patch(url, data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "created_at" in response.json()[0]
