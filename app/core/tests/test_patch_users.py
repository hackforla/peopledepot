from core.api.validate_request import validate_patch_fields
import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from test_data.utils.seed_constants import garry_name, valerie_name, wanda_admin_project
from test_data.utils.seed_user import SeedUser

def _call_api(requesting_user_name, response_related_name, data):
    requester = SeedUser.get_user(requesting_user_name)
    client = APIClient()
    client.force_authenticate(user=requester)

    response_related_user = SeedUser.get_user(response_related_name)
    url = reverse("user-detail", args=[response_related_user.uuid])
    data = data
    return client.patch(url, data, format="json")


@pytest.mark.django_db
class TestPatchUser:
    def test_patch_request_calls_validate_request(self, mocker):
        requester = SeedUser.get_user(garry_name)
        client = APIClient()
        client.force_authenticate(user=requester)
        response_related_user = SeedUser.get_user(valerie_name)
        url = reverse("user-detail", args=[response_related_user.uuid])
        data = {
            "last_name": "Updated",
            "email_gmail": "update@example.com",
        }

        mock_validate_patch = mocker.patch("core.api.has_user_permissions.validate_patch_fields")
        client.patch(url, data, format="json")

        # Assert it was called
        mock_validate_patch.assert_called_once()
        __args__, kwargs = mock_validate_patch.call_args
        request_received = kwargs.get("request")
        response_related_user_received = kwargs.get("obj")

        assert request_received.data == data
        assert request_received.user == requester
        assert response_related_user_received == response_related_user

    def test_valid_patch(self):
        patch_data = {
            "last_name": "Foo",
            # "email_gmail": "smith@example.com",
            # "first_name": "John",
        }
        response = _call_api(
            requesting_user_name=garry_name,
            response_related_name=wanda_admin_project,
            data=patch_data,
        )
        assert response.status_code == status.HTTP_200_OK, response.data

    def test_patch_with_not_permitted_fields(self):
        """Test patch request returns 400 response when request fields do not match configured fields.

        Fields are configured to not include last_name.  The test will attempt to create a user
        with last_name in the request data.  The test should fail with a 400 status code.

        See documentation for test_allowable_patch_fields_configurable for more information.
        """

        patch_data = {
            "email_gmail": "smith@example.com",
            "created_at": "2022-01-01T00:00:00Z",
        }
        response = _call_api(
            requesting_user_name=garry_name,
            response_related_name=wanda_admin_project,
            data=patch_data,
        )
        response = _call_api(
            requesting_user_name=garry_name,
            response_related_name=wanda_admin_project,
            data=patch_data,
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_patch_with_unprivileged_requesting_user(self):
        """Test patch request returns 400 response when request fields do not match configured fields.

        Fields are configured to not include last_name.  The test will attempt to create a user
        with last_name in the request data.  The test should fail with a 400 status code.

        See documentation for test_allowable_patch_fields_configurable for more information.
        """

        patch_data = {
            "email_gmail": "smith@example.com",
        }
        response = _call_api(
            requesting_user_name=wanda_admin_project,
            response_related_name=valerie_name,
            data=patch_data,
        )
        response = _call_api(
            requesting_user_name=wanda_admin_project,
            response_related_name=valerie_name,
            data=patch_data,
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
