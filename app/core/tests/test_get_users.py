import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from constants import admin_project
from constants import member_project
from core.api.permission_validation import PermissionValidation
from core.tests.utils.seed_constants import valerie_name
from core.tests.utils.seed_constants import wally_name
from core.tests.utils.seed_constants import wanda_admin_project
from core.tests.utils.seed_constants import winona_name
from core.tests.utils.seed_user import SeedUser

count_website_members = 5
count_people_depot_members = 3
count_members_either = 6

_user_get_url = reverse("user-list")


@pytest.mark.django_db
@pytest.mark.load_user_data_required  # see load_user_data_required in conftest.py
class TestGetUser:
    @staticmethod
    def _get_response_fields(first_name, response_data):
        response_related_user = None

        # look up target user in response_data by first name
        for user in response_data:
            if user["first_name"] == first_name:
                response_related_user = user
                break


        # Throw error if target user not found
        if response_related_user == None:
            raise ValueError(
                "Test set up mistake.  No user with first name of ${first_name}"
            )

        # Otherwise check if user fields in response data are the same as fields
        return set(user)

    def test_get_url_results_for_admin_project(self):
        """Test that the get user request returns (a) all users on the website project
        and (b) the fields match fields configured for a project admin
        **WHEN** the requesting_user is a project admin.
        """
        client = APIClient()
        client.force_authenticate(user=SeedUser.get_user(wanda_admin_project))
        response = client.get(_user_get_url)
        assert response.status_code == 200
        assert len(response.json()) == count_website_members
        response_fields = self._get_response_fields(winona_name, response.data)
        valid_fields = PermissionValidation.get_fields(operation="get", permission_type=admin_project, table_name="user")
        assert response_fields == set(valid_fields)

    def test_get_results_for_users_on_same_team(self):
        """Test that get user request (a) returns users on the website project
        and (b) the fields returned match the configured fields for
        the team member permission type **WHEN** the requuster is a team member
        of the web site project.
        """
        client = APIClient()
        client.force_authenticate(user=SeedUser.get_user(wally_name))
        response = client.get(_user_get_url)

        assert response.status_code == 200
        assert len(response.json()) == count_website_members
        response_fields = self._get_response_fields(winona_name, response.data)
        valid_fields = PermissionValidation.get_fields(operation="get", permission_type=member_project, table_name="user")
        assert response_fields == set(valid_fields)
        assert len(response.json()) == count_website_members

    def test_no_user_permission(self):
        """Test that get user request returns no data when requesting_user has no permissions."""
        client = APIClient()
        client.force_authenticate(user=SeedUser.get_user(valerie_name))
        response = client.get(_user_get_url)
        assert response.status_code == 200
        assert len(response.json()) == 0
