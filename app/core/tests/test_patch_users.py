import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


# from core.api.permission_validation import PermissionValidation
# from core.models import User
from core.tests.utils.seed_constants import garry_name
from core.tests.utils.seed_constants import valerie_name

from core.api.user_request import UserRequest
from core.tests.utils.seed_user import SeedUser
from unittest.mock import patch

count_website_members = 4
count_people_depot_members = 3
count_members_either = 6


@pytest.mark.django_db
@pytest.mark.load_user_data_required  # see load_user_data_required in conftest.py
class TestPatchUser:

    @patch.object(UserRequest, "validate_fields")
    def test_patch_request_calls_validate_request(self, mock_validate_user_related_request):
        """Test that the patch requests succeeds when the requester is an admin."""
        requester = SeedUser.get_user(garry_name)
        client = APIClient()
        client.force_authenticate(user=requester)

        response_related_user = SeedUser.get_user(valerie_name)
        url = reverse("user-detail", args=[response_related_user.uuid])
        data = {
            "last_name": "Updated",
            "gmail": "update@example.com",
        }
        client.patch(url, data, format="json")
        __args__, kwargs = mock_validate_user_related_request.call_args
        request_received = kwargs.get("request")
        response_related_user_received = kwargs.get("response_related_user")
        assert request_received.data == data
        assert request_received.user == requester
        assert response_related_user_received == response_related_user
        # assert (
        #     response.status_code == status.HTTP_200_OK
        # ), f"API Error: {response.status_code} - {response.content.decode()}"
        # assert len(response.data) == len(User.object.all())

    def test_admin_cannot_patch_created_at(self):
        """Test that the patch request raises a validation exception
        when the request fields includes created_date, even if the
        requester is an admin.
        """
        requester = SeedUser.get_user(garry_name)
        client = APIClient()
        client.force_authenticate(user=requester)

        response_related_user = SeedUser.get_user(valerie_name)
        url = reverse("user-detail", args=[response_related_user.uuid])
        data = {
            "created_at": "2022-01-01T00:00:00Z",
        }
        response = client.patch(url, data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "created_at" in response.json()[0]

