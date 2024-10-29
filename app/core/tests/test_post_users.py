import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate

from constants import admin_global
from core.api.cru import Cru
from core.api.views import UserViewSet
from core.tests.utils.seed_constants import garry_name, wanda_admin_project
from core.tests.utils.seed_user import SeedUser

count_website_members = 4
count_people_depot_members = 3
count_members_either = 6




@pytest.mark.django_db
@pytest.mark.load_user_data_required  # see load_user_data_required in conftest.py
class TestPostUser:
    @staticmethod
    def _post_request_to_viewset(requester, create_data):
        new_data = create_data.copy()
        factory = APIRequestFactory()
        request = factory.post(reverse("user-list"), data=new_data, format="json")
        force_authenticate(request, user=requester)
        view = UserViewSet.as_view({"post": "create"})
        response = view(request)
        return response
    
    @classmethod
    def test_valid_post(self):
        """Test POST request returns success when the request fields match configured fields.

        This test mocks a PATCH request to skip submitting the request to the server and instead
        calls the view directly with the request.  This is done so that variables used by the
        server can be set to test values.
        """
        requester = SeedUser.get_user(garry_name)  # project lead for website

        create_data = {
            "username": "foo",
            "last_name": "Smith",
            "first_name": "John",
            "gmail": "smith@example.com",
            "time_zone": "America/Los_Angeles",
            "password": "password",
            "first_name": "John",
        }
        response = TestPostUser._post_request_to_viewset(requester, create_data)

        assert response.status_code == status.HTTP_201_CREATED

    def test_post_with_not_allowed_fields(self):
        """Test post request returns 400 response when request fields do not match configured fields.

        Fields are configured to not include last_name.  The test will attempt to create a user
        with last_name in the request data.  The test should fail with a 400 status code.

        See documentation for test_allowable_patch_fields_configurable for more information.
        """

        requester = SeedUser.get_user(garry_name)  # project lead for website
        post_data = {
            "username": "foo",
            "first_name": "Mary",
            "last_name": "Smith",
            "gmail": "smith@example.com",
            "time_zone": "America/Los_Angeles",
            "password": "password",
            "first_name": "John",
            "created_at": "2022-01-01T00:00:00Z",
        }
        response = TestPostUser._post_request_to_viewset(requester, post_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_post_with_unprivileged_requester(self):
        """Test post request returns 400 response when request fields do not match configured fields.

        Fields are configured to not include last_name.  The test will attempt to create a user
        with last_name in the request data.  The test should fail with a 400 status code.

        See documentation for test_allowable_patch_fields_configurable for more information.
        """

        requester = SeedUser.get_user(wanda_admin_project)  # project lead for website
        post_data = {
            "username": "foo",
            "first_name": "Mary",
            "last_name": "Smith",
            "gmail": "smith@example.com",
            "time_zone": "America/Los_Angeles",
            "password": "password",
            "first_name": "John",
            "created_at": "2022-01-01T00:00:00Z",
        }
        response = TestPostUser._post_request_to_viewset(requester, post_data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
