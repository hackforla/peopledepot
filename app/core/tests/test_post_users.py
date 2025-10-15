import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate

from core.api.views import UserViewSet
from core.models import User
from test_data.utils.seed_constants import garry_name
from test_data.utils.seed_constants import wanda_admin_project
from test_data.utils.seed_user import SeedUser

count_website_members = 4
count_people_depot_members = 3
count_members_either = 6


@pytest.mark.django_db
class TestPostUser:
    @staticmethod
    def _post_request_to_viewset(requesting_user, create_data):
        new_data = create_data.copy()
        factory = APIRequestFactory()
        request = factory.post(reverse("user-list"), data=new_data, format="json")
        force_authenticate(request, user=requesting_user)
        view = UserViewSet.as_view({"post": "create"})
        response = view(request)
        return response

    @classmethod
    def test_valid_post(cls):
        """Test POST request returns success when the request fields match configured fields.

        This test calls the UserViewSet directly with the request.
        """
        requesting_user = SeedUser.get_user(garry_name)  # project lead for website

        create_data = {
            "username": "foo",
            "last_name": "Smith",
            "first_name": "John",
            "email_gmail": "smith@example.com",
            "time_zone": "America/Los_Angeles",
        }
        response = cls._post_request_to_viewset(requesting_user, create_data)

        assert response.status_code == status.HTTP_201_CREATED, response.data

    def test_post_with_not_permitted_fields(self):
        """Test post request returns 400 response when request fields do not match configured fields.

        Fields are configured to not include last_name.  The test will attempt to create a user
        with last_name in the request data.  The test should fail with a 400 status code.

        See documentation for test_allowable_patch_fields_configurable for more information.
        """

        requesting_user = SeedUser.get_user(garry_name)  # project lead for website
        post_data = {
            "username": "foo",
            "first_name": "Mary",
            "last_name": "Smith",
            "email_gmail": "smith@example.com",
            "time_zone": "America/Los_Angeles",
            "password": "password",
            "created_at": "2022-01-01T00:00:00Z",
        }
        response = TestPostUser._post_request_to_viewset(requesting_user, post_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_post_with_unprivileged_requesting_user(self):
        """Test post request returns 400 response when request fields do not match configured fields.

        Fields are configured to not include last_name.  The test will attempt to create a user
        with last_name in the request data.  The test should fail with a 400 status code.

        See documentation for test_allowable_patch_fields_configurable for more information.
        """

        requesting_user = SeedUser.get_user(
            wanda_admin_project
        )  # project lead for website
        post_data = {
            "username": "foo",
            "first_name": "Mary",
            "last_name": "Smith",
            "email_gmail": "smith@example.com",
            "time_zone": "America/Los_Angeles",
            "password": "password",
            "created_at": "2022-01-01T00:00:00Z",
        }
        response = TestPostUser._post_request_to_viewset(requesting_user, post_data)
        assert response.status_code == status.HTTP_403_FORBIDDEN
