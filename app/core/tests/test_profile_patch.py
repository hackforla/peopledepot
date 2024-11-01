import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from core.api.user_request import UserRequest
from core.tests.utils.seed_user import SeedUser
from unittest.mock import patch

from core.tests.utils.seed_constants import garry_name, wanda_admin_project, valerie_name
from core.tests.utils.seed_user import SeedUser


@pytest.mark.django_db
@pytest.mark.load_user_data_required  # see load_user_data_required in conftest.py
class TestPatchProfile:

    @staticmethod
    def _call_api(requesting_user_name, data):
        requester = SeedUser.get_user(requesting_user_name)
        client = APIClient()
        client.force_authenticate(user=requester)
        url = reverse("my_profile")
        data = data
        return client.patch(url, data, format="json")


    @classmethod
    def test_profile_with_valid_fields(cls):
        patch_data = {
            "last_name": "Foo",
            # "gmail": "smith@example.com",
            # "first_name": "John",
        }
        response = cls._call_api(requesting_user_name=garry_name, data=patch_data)
        assert response.status_code == status.HTTP_200_OK

    def test_profile_patch_with_not_allowed_fields(cls):
        """Test patch request returns 400 response when request fields do not match configured fields.

        Fields are configured to not include last_name.  The test will attempt to create a user
        with last_name in the request data.  The test should fail with a 400 status code.

        See documentation for test_allowable_patch_fields_configurable for more information.
        """

        patch_data = {
            "gmail": "smith@example.com",
            "created_at": "2022-01-01T00:00:00Z",
        }
        response = cls._call_api(requesting_user_name=garry_name, data=patch_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

