import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.test import APIClient
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate

from constants import global_admin
from constants import project_lead
from core.api.views import UserViewSet
from core.field_permissions2 import FieldPermissions2
from core.permission_util import PermissionUtil
from core.tests.utils.seed_constants import garry_name
from core.tests.utils.seed_constants import wanda_name
from core.tests.utils.seed_user import SeedUser

count_website_members = 4
count_people_depot_members = 3
count_members_either = 6


def post_request_to_viewset(requester, create_data):
    new_data = create_data.copy()
    factory = APIRequestFactory()
    request = factory.post(reverse("user-list"), data=new_data, format="json")
    force_authenticate(request, user=requester)
    view = UserViewSet.as_view({"post": "create"})
    response = view(request)
    return response


@pytest.mark.django_db
class TestPostUser:
    def setup_method(self):
        FieldPermissions2.derive_cru_fields()

    def teardown_method(self):
        FieldPermissions2.derive_cru_fields()

    def test_admin_post_request_succeeds(self):  #
        requester = SeedUser.get_user(garry_name)
        client = APIClient()
        client.force_authenticate(user=requester)

        url = reverse("user-list")
        data = {
            "username": "createuser",
            "last_name": "created",
            "gmail": "create@example.com",
            "password": "password",
        }
        response = client.post(url, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED

    def test_admin_post_with_created_at_fails(self):
        requester = SeedUser.get_user(garry_name)
        client = APIClient()
        client.force_authenticate(user=requester)

        url = reverse("user-list")
        data = {
            "username": "createuser",
            "last_name": "created",
            "gmail": "create@example.com",
            "password": "password",
            "time_zone": "America/Los_Angeles",
            "created_at": "2022-01-01T00:00:00Z",
        }
        response = client.post(url, data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_validate_fields_postable_raises_exception_for_created_at(self):
        with pytest.raises(ValidationError):
            PermissionUtil.validate_fields_postable(
                SeedUser.get_user(garry_name),
                ["created_at"],
            )

    def test_validate_fields_postable_raises_exception_for_project_lead(self):
        with pytest.raises(PermissionError):
            PermissionUtil.validate_fields_postable(
                SeedUser.get_user(wanda_name), ["username", "password"]
            )

    def test_allowable_post_fields_configurable(self):
        """Test that the fields that can be updated are configurable.

        This test mocks a PATCH request to skip submitting the request to the server and instead
        calls the view directly with the request.  This is done so that variables used by the
        server can be set to test values.
        """

        FieldPermissions2.user_post_fields[global_admin] = [
            "username",
            "first_name",
            "last_name",
            "gmail",
            "time_zone",
            "password",
            "created_at",
        ]

        requester = SeedUser.get_user(garry_name)  # project lead for website

        create_data = {
            "username": "foo",
            "last_name": "Smith",
            "gmail": "smith@example.com",
            "time_zone": "America/Los_Angeles",
            "password": "password",
            "first_name": "John",
            "created_at": "2022-01-01T00:00:00Z",
        }
        response = post_request_to_viewset(requester, create_data)

        assert response.status_code == status.HTTP_201_CREATED

    def test_not_allowable_post_fields_configurable(self):
        """Test that the fields that are not configured to be updated cannot be updated.

        See documentation for test_allowable_patch_fields_configurable for more information.
        """

        FieldPermissions2.user_post_fields[global_admin] = [
            "username",
            "first_name",
            "gmail",
            "time_zone",
            "password",
            "created_at",
        ]

        requester = SeedUser.get_user(garry_name)  # project lead for website

        post_data = {
            "username": "foo",
            "last_name": "Smith",
            "gmail": "smith@example.com",
            "time_zone": "America/Los_Angeles",
            "password": "password",
            "first_name": "John",
            "created_at": "2022-01-01T00:00:00Z",
        }
        response = post_request_to_viewset(requester, post_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
