import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate

from constants import admin_project
from core.api.views import UserViewSet
from core.field_permissions import FieldPermissions
from core.tests.utils.load_data import load_data
from core.tests.utils.seed_constants import garry_name
from core.tests.utils.seed_constants import valerie_name
from core.tests.utils.seed_constants import wally_name
from core.tests.utils.seed_constants import wanda_admin_project
from core.tests.utils.seed_user import SeedUser

count_website_members = 4
count_people_depot_members = 3
count_members_either = 6


def fields_match(first_name, user_data, fields):
    for user in user_data:
        if user["first_name"] == first_name:
            return set(user.keys()) == set(fields)
    return False


def patch_request_to_viewset(requester, target_user, update_data):
    factory = APIRequestFactory()
    request = factory.patch(
        reverse("user-detail", args=[target_user.uuid]), update_data, format="json"
    )
    force_authenticate(request, user=requester)
    view = UserViewSet.as_view({"patch": "partial_update"})
    response = view(request, uuid=requester.uuid)
    return response


@pytest.mark.django_db
class TestPatchUser:
    # Some tests change FieldPermission attribute values.
    # derive_cru resets the values before each test - otherwise
    # the tests would interfere with each other
    def setup_method(self):
        FieldPermissions.derive_cru_fields()
        load_data()

    # Some tests change FieldPermission attribute values.
    # derive_cru resets the values after each test
    # Redundant with setup_method, but good practice
    def teardown_method(self):
        FieldPermissions.derive_cru_fields()

    def test_admin_patch_request_succeeds(self):
        """Test that the patch requests succeeds when the requester is an admin."""
        requester = SeedUser.get_user(garry_name)
        client = APIClient()
        client.force_authenticate(user=requester)

        target_user = SeedUser.get_user(valerie_name)
        url = reverse("user-detail", args=[target_user.uuid])
        data = {
            "last_name": "Updated",
            "gmail": "update@example.com",
        }
        response = client.patch(url, data, format="json")
        assert response.status_code == status.HTTP_200_OK

    def test_admin_cannot_patch_created_at(self):
        """Test that the patch request raises a validation exception
        when the request fields includes created_date, even if the
        requester is an admin.
        """
        requester = SeedUser.get_user(garry_name)
        client = APIClient()
        client.force_authenticate(user=requester)

        target_user = SeedUser.get_user(valerie_name)
        url = reverse("user-detail", args=[target_user.uuid])
        data = {
            "created_at": "2022-01-01T00:00:00Z",
        }
        response = client.patch(url, data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "created_at" in response.json()[0]

    def test_allowable_patch_fields_configurable(self):
        """Test that the fields that can be updated are configurable.

        This test mocks a PATCH request to skip submitting the request to the server and instead
        calls the view directly with the request.  This is done so that variables used by the
        server can be set to test values.
        """

        FieldPermissions.user_patch_fields[admin_project] = ["last_name", "gmail"]

        requester = SeedUser.get_user(wanda_admin_project)  # project lead for website
        update_data = {"last_name": "Smith", "gmail": "smith@example.com"}
        target_user = SeedUser.get_user(wally_name)
        response = patch_request_to_viewset(requester, target_user, update_data)

        assert response.status_code == status.HTTP_200_OK

    def test_not_allowable_patch_fields_configurable(self):
        """Test that the fields that are not configured to be updated cannot be updated.

        See documentation for test_allowable_patch_fields_configurable for more information.
        """

        requester = SeedUser.get_user(wanda_admin_project)  # project lead for website
        FieldPermissions.user_patch_fields[admin_project] = ["gmail"]
        update_data = {"last_name": "Smith"}
        target_user = SeedUser.get_user(wally_name)
        response = patch_request_to_viewset(requester, target_user, update_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
