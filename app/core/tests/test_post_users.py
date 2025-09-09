import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from core.api.request_fields_allowed import RequestFieldsAllowed
from constants import admin_project
from constants import member_project
from core.tests.utils.seed_constants import valerie_name
from core.tests.utils.seed_constants import wally_name
from core.tests.utils.seed_constants import wanda_admin_project
from core.tests.utils.seed_constants import winona_name
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

    Verifies that users are returned according to project and team membership,
    and that the fields returned comply with the requesting user's permission level.
    """

    @staticmethod
    def _get_response_fields(first_name: str, response_data: list[dict]) -> set:
        """
        Extract the set of fields returned for a user with a given first name.

        Args:
            first_name (str): The first name of the user to search for in the response data.
            response_data (list[dict]): The JSON-decoded response data from GET /users.

        Returns:
            set: The set of keys (field names) present for the target user.

        Raises:
            ValueError: If no user with the specified first name is found in the response.
        """
        response_related_user = None

        for user in response_data:
            if user["first_name"] == first_name:
                response_related_user = user
                break

        if response_related_user is None:
            raise ValueError(
                f"Test set up mistake. No user with first name of {first_name}"
            )

        return set(response_related_user)

    def _perform_get_request(self, requesting_user: str) -> tuple[int, list[dict]]:
        """
        Helper method to perform an authenticated GET request to the user list endpoint.

        Args:
            requesting_user (str): The first name of the user to authenticate as.

        Returns:
            tuple: A tuple containing the HTTP status code and the JSON-decoded response data.
        """
        client = APIClient()
        client.force_authenticate(user=SeedUser.get_user(requesting_user))
        response = client.get(_USER_GET_URL)
        return response.status_code, response.json()

    def test_get_url_results_for_admin_project(self):
        """
        Test GET /users for a project admin.

        Verifies that:
        - All users on the website project are returned.
        - The returned fields match those allowed for a project admin.
        """
        status_code, response_data = self._perform_get_request(wanda_admin_project)
        assert status_code == 200
        assert len(response_data) == COUNT_WEBSITE_MEMBERS

        response_fields = self._get_response_fields(winona_name, response_data)
        valid_fields = RequestFieldsAllowed._get_permitted_fields(
            operation="get", permission_type=admin_project, table_name="User"
        )
        assert response_fields == set(valid_fields)

    def test_get_results_for_users_on_same_team(self):
        """
        Test GET /users for a team member.

        Verifies that:
        - Only users on the same project/team are returned.
        - The returned fields comply with the member permission configuration.
        """
        status_code, response_data = self._perform_get_request(wally_name)
        assert status_code == 200
        assert len(response_data) == COUNT_WEBSITE_MEMBERS

        response_fields = self._get_response_fields(winona_name, response_data)
        valid_fields = RequestFieldsAllowed._get_permitted_fields(
            operation="get", permission_type=member_project, table_name="User"
        )
        assert response_fields == set(valid_fields)

    def test_no_user_permission(self):
        """
        Test GET /users when the requesting user has no permissions.

        Verifies that:
        - The response succeeds with status 200.
        - No user data is returned.
        """
        status_code, response_data = self._perform_get_request(valerie_name)
        assert status_code == 200
        assert len(response_data) == 0
