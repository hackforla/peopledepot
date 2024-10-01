import pytest
from django.urls import reverse
from rest_framework.exceptions import ValidationError
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate

from core.api.views import UserViewSet
from core.permission_check import PermissionCheck
from core.tests.utils.load_data import load_data
from core.tests.utils.seed_constants import garry_name
from core.tests.utils.seed_constants import wanda_admin_project
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
        load_data()

    def test_validate_fields_postable_raises_exception_for_created_at(self):
        """Test validate_fields_postable raises ValidationError when requesting
        fields includes created_at.
        """
        with pytest.raises(ValidationError):
            PermissionCheck.validate_fields_postable(
                SeedUser.get_user(garry_name),
                ["created_at"],
            )

    def test_validate_fields_postable_raises_exception_for_admin_project(self):
        """Test validate_fields_postable raises PermissionError when requesting
        user is a project lead and fields include password
        """
        with pytest.raises(PermissionError):
            PermissionCheck.validate_fields_postable(
                SeedUser.get_user(wanda_admin_project), ["username", "password"]
            )