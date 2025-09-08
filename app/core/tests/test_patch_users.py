from unittest.mock import patch

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from core.api.user_related_request import UserRelatedRequest
from core.tests.utils.seed_constants import garry_name, valerie_name, wanda_admin_project
from core.tests.utils.seed_user import SeedUser


@pytest.mark.django_db
@pytest.mark.load_user_data_required
class TestPatchUser:
    """
    Test suite for PATCH /users/<uuid> endpoint.

    Ensures that:
    - Requests are validated according to the requesting user's permission.
    - Users can only patch allowed fields.
    - Responses match expected status codes for success and failure cases.
    """

    @staticmethod
    def _call_api(requesting_user_name: str, response_related_name: str, data: dict):
        """
        Helper method to send an authenticated PATCH request to a specific user's endpoint.

        Args:
            requesting_user_name (str): First name of the user making the request.
            response_related_name (str): First name of the user being updated.
            data (dict): Dictionary containing the fields to patch.

        Returns:
            Response: The DRF Response object from the PATCH request.
        """
        requester = SeedUser.get_user(requesting_user_name)
        client = APIClient()
        client.force_authenticate(user=requester)

        response_related_user = SeedUser.get_user(response_related_name)
        url = reverse("user-detail", args=[response_related_user.uuid])
        return client.patch(url, data, format="json")

    @patch.object(UserRelatedRequest, UserRelatedRequest.validate_patch_fields.__name__)
    def test_patch_request_calls_validate_request(self, mock_validate_fields):
        """
        Verify that PATCH request calls `validate_patch_fields` for field validation.

        Ensures that:
        - The request data is passed correctly to validation.
        - The requesting user and target user are passed to validation.
        """
        requester = SeedUser.get_user(garry_name)
        client = APIClient()
        client.force_authenticate(user=requester)

        response_related_user = SeedUser.get_user(valerie_name)
        url = reverse("user-detail", args=[response_related_user.uuid])
        data = {"last_name": "Updated", "email_gmail": "update@example.com"}
        client.patch(url, data, format="json")

        __args__, kwargs = mock_validate_fields.call_args
        request_received = kwargs.get("request")
        response_related_user_received = kwargs.get("obj")

        assert request_received.data == data
        assert request_received.user == requester
        assert response_related_user_received == response_related_user

    @classmethod
    def test_valid_patch(cls):
        """
        Verify that a valid PATCH request by an authorized user succeeds.

        Sends a PATCH request with allowed fields and expects a 200 OK response.
        """
        patch_data = {"last_name": "Foo"}
        response = cls._call_api(
            requesting_user_name=garry_name,
            response_related_name=wanda_admin_project,
            data=patch_data,
        )
        assert response.status_code == status.HTTP_200_OK

    @classmethod
    def test_patch_with_not_allowed_fields(cls):
        """
        Verify that PATCH request with disallowed fields returns 400 Bad Request.

        Fields in the request that are not permitted should trigger a validation error.
        """
        patch_data = {"email_gmail": "smith@example.com", "created_at": "2022-01-01T00:00:00Z"}
        response = cls._call_api(
            requesting_user_name=garry_name,
            response_related_name=wanda_admin_project,
            data=patch_data,
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @classmethod
    def test_patch_with_unprivileged_requesting_user(cls):
        """
        Verify that PATCH request by a user without permission returns 404 Not Found.

        Attempting to patch a user the requester cannot access should result in a 404.
        """
        patch_data = {"email_gmail": "smith@example.com"}
        response = cls._call_api(
            requesting_user_name=wanda_admin_project,
            response_related_name=valerie_name,
            data=patch_data,
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND
