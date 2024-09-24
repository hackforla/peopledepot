import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate

from constants import admin_global
from core.api.views import UserViewSet
from core.field_permissions import FieldPermissions
from core.tests.utils.load_data import load_data
from core.tests.utils.seed_constants import garry_name
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


# @pytest.fixture(scope='class', autouse=True)
# def special_data_setup(db):  # Use the db fixture to enable database access
#     # Load your special data here
#     call_command('load_data_command')  # Replace with your command
#     yield


@pytest.mark.django_db
class TestPostUser:
    def setup_method(self):
        FieldPermissions.derive_cru_fields()
        load_data()

    def teardown_method(self):
        FieldPermissions.derive_cru_fields()

    def test_allowable_post_fields_configurable(self):
        """Test POST request returns success when the request fields match configured fields.

        This test mocks a PATCH request to skip submitting the request to the server and instead
        calls the view directly with the request.  This is done so that variables used by the
        server can be set to test values.
        """

        FieldPermissions.user_post_fields[admin_global] = [
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
        """Test post request returns 400 response when request fields do not match configured fields.

        Fields are configured to not include last_name.  The test will attempt to create a user
        with last_name in the request data.  The test should fail with a 400 status code.

        See documentation for test_allowable_patch_fields_configurable for more information.
        """

        FieldPermissions.user_post_fields[admin_global] = [
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
