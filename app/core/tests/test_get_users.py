import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from constants import admin_project, member_project
from core.api.permission_validation import PermissionValidation
from core.tests.utils.seed_constants import valerie_name, wally_name, wanda_admin_project, winona_name
from core.tests.utils.seed_user import SeedUser

# Constants representing expected user counts in tests
COUNT_WEBSITE_MEMBERS = 5
COUNT_PEOPLE_DEPOT_MEMBERS = 3
COUNT_MEMBERS_EITHER = 6

_USER_GET_URL = reverse("user-list")


@pytest.mark.django_db
@pytest.mark.load_user_data_required
class TestGetUser:
    """
    Test suite for the User GET API endpoint.

    Ensures that:
    - Users are returned according to project and team membership.
    - Returned fields respect the configured permissions for the requesting user.
    """

    @staticmethod
    def _get_response_fields(first_name: str, response_data: list[dict]) -> set:
        """
        Retrieve the set of fields from the user with the given first name in the response data.

        Args:
            first_name (str): First name of the target user.
            response_data (list[dict]): JSON-decoded response data from GET /users.

        Returns:
            set: The set of keys (fields) present for the target user in the response.

        Raises:
            ValueError: If no user with the specified first name is found.
        """
        response_related_user = None

        # look up target user in response_data by first name
        for user in response_data:
            if user["first_name"] == first_name:
                response_related_user = user
                break

        # Throw error if target user not found
        if response_related_user is None:
            raise ValueError(f"Test set up mistake. No user with first name of {first_name}")

        # Otherwise check if user fields in response data are the same as fields
        return set(response_related_user)

    def test_get_url_results_for_admin_project(self):
        """
        Verify GET /users for a project admin.

        Ensures that:
        - All users on the website project are returned.
        - Returned fields match the admin permission configuration.
        """
        client = APIClient()
        client.force_authenticate(user=SeedUser.get_user(wanda_admin_project))
        response = client.get(_USER_GET_URL)

        assert response.status_code == 200
        assert len(response.json()) == COUNT_WEBSITE_MEMBERS

        response_fields = self._get_response_fields(winona_name, response.data)
        valid_fields = PermissionValidation.get_permitted_fields(
            operation="get", permission_type=admin_project, table_name="User"
        )
        assert response_fields == set(valid_fields)

    def test_get_results_for_users_on_same_team(self):
        """
        Verify GET /users for a team member.

        Ensures that:
        - Only users on the same project/team are returned.
        - Returned fields match the member permission configuration.
        """
        client = APIClient()
        client.force_authenticate(user=SeedUser.get_user(wally_name))
        response = client.get(_USER_GET_URL)

        assert response.status_code == 200
        assert len(response.json()) == COUNT_WEBSITE_MEMBERS

        response_fields = self._get_response_fields(winona_name, response.data)
        valid_fields = PermissionValidation.get_permitted_fields(
            operation="get", permission_type=member_project, table_name="User"
        )
        assert response_fields == set(valid_fields)

    def test_no_user_permission(self):
        """
        Verify GET /users when the requesting user has no permissions.

        Ensures that:
        - The response is successful (status 200).
        - No user data is returned.
        """
        client = APIClient()
        client.force_authenticate(user=SeedUser.get_user(valerie_name))
        response = client.get(_USER_GET_URL)

        assert response.status_code == 200
        assert len(response.json()) == 0
