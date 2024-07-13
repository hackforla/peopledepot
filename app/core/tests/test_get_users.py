import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from constants import global_admin
from constants import project_member
from core.field_permissions import FieldPermissions
from core.tests.utils.seed_constants import valerie_name
from core.tests.utils.seed_constants import wally_name
from core.tests.utils.seed_constants import wanda_project_lead
from core.tests.utils.seed_constants import winona_name
from core.tests.utils.seed_user import SeedUser

count_website_members = 4
count_people_depot_members = 3
count_members_either = 6

_user_get_url = reverse("user-list")


def fields_match_for_get_user(first_name, response_data, fields):
    for user in response_data:
        if user["first_name"] == first_name:
            return set(user.keys()) == set(fields)
    return False


@pytest.mark.django_db
class TestGetUser:
    def test_get_url_results_for_project_admin(self):
        """Test that the get user request returns (a) all users on the website project
        and (b) the fields match fields configured for a project admin
        **WHEN** the requester is a project admin.
        """
        client = APIClient()
        client.force_authenticate(user=SeedUser.get_user(wanda_project_lead))
        response = client.get(_user_get_url)
        assert response.status_code == 200
        assert len(response.json()) == count_website_members
        assert fields_match_for_get_user(
            winona_name,
            response.json(),
            FieldPermissions.user_read_fields[global_admin],
        )

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
        assert fields_match_for_get_user(
            winona_name,
            response.json(),
            FieldPermissions.user_read_fields[project_member],
        )
        assert fields_match_for_get_user(
            wanda_project_lead,
            response.json(),
            FieldPermissions.user_read_fields[project_member],
        )
        assert len(response.json()) == count_website_members

    def test_no_user_permission(self):
        """Test that get user request returns no data when requester has no permissions."""
        client = APIClient()
        client.force_authenticate(user=SeedUser.get_user(valerie_name))
        response = client.get(_user_get_url)
        assert response.status_code == 200
        assert len(response.json()) == 0
