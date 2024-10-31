import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from core.api.user_request import UserRequest
from core.tests.utils.seed_user import SeedUser
from unittest.mock import patch


from core.api.views import UserViewSet
from core.tests.utils.seed_constants import garry_name, wanda_admin_project, valerie_name
from core.tests.utils.seed_user import SeedUser


@pytest.mark.django_db
@pytest.mark.load_user_data_required  # see load_user_data_required in conftest.py
class TestPatchUser:
    # @staticmethod
    # def _patch_request_to_viewset(requesting_user, patch_data):
    #     new_data = patch_data.copy()
    #     factory = APIRequestFactory()
    #     request = factory.patch(reverse("user-detail"), data=new_data, format="json")
    #     force_authenticate(request, user=requesting_user)
    #     view = UserViewSet.as_view({"patch": "partial_update"})
    #     response = view(request)
    #     return response
    @staticmethod
    def _call_api(requesting_user_name, response_related_name, data):
        requester = SeedUser.get_user(requesting_user_name)
        client = APIClient()
        client.force_authenticate(user=requester)

        response_related_user = SeedUser.get_user(response_related_name)
        url = reverse("user-detail", args=[response_related_user.uuid])
        data = data
        return client.patch(url, data, format="json")

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

    @classmethod
    def test_valid_patch(cls):
        patch_data = {
            "last_name": "Foo",
            # "gmail": "smith@example.com",
            # "first_name": "John",
        }
        response = cls._call_api(requesting_user_name=garry_name, response_related_name=wanda_admin_project,data=patch_data)
        assert response.status_code == status.HTTP_200_OK

    def test_patch_with_not_allowed_fields(cls):
        """Test patch request returns 400 response when request fields do not match configured fields.

        Fields are configured to not include last_name.  The test will attempt to create a user
        with last_name in the request data.  The test should fail with a 400 status code.

        See documentation for test_allowable_patch_fields_configurable for more information.
        """

        patch_data = {
            "gmail": "smith@example.com",
            "created_at": "2022-01-01T00:00:00Z",
        }
        response = cls._call_api(requesting_user_name=garry_name, response_related_name=wanda_admin_project, data=patch_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_patch_with_unprivileged_requesting_user(cls):
        """Test patch request returns 400 response when request fields do not match configured fields.

        Fields are configured to not include last_name.  The test will attempt to create a user
        with last_name in the request data.  The test should fail with a 400 status code.

        See documentation for test_allowable_patch_fields_configurable for more information.
        """

        patch_data = {
            "gmail": "smith@example.com",
        }
        response = cls._call_api(requesting_user_name=wanda_admin_project, response_related_name=valerie_name, data=patch_data)
        assert response.status_code == status.HTTP_404_NOT_FOUND
