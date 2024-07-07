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
from core.base_user_cru_constants import user_field_permissions
from core.derived_user_cru_permissions import derive_cru_fields
from core.derived_user_cru_permissions import user_create_fields
from core.permission_util import PermissionUtil
from core.tests.utils.seed_constants import garry_name
from core.tests.utils.seed_constants import patti_name
from core.tests.utils.seed_constants import valerie_name
from core.tests.utils.seed_constants import wally_name
from core.tests.utils.seed_constants import wanda_name
from core.tests.utils.seed_constants import winona_name
from core.tests.utils.seed_constants import zani_name
from core.tests.utils.seed_user import SeedUser

count_website_members = 4
count_people_depot_members = 3
count_members_either = 6


def post_request_to_view(requester, target_user, create_data):
    factory = APIRequestFactory()
    request = factory.post(
        reverse("user-detail", args=[target_user.uuid]), create_data, format="json"
    )
    force_authenticate(request, user=requester)
    view = UserViewSet.as_view({"post": "create"})
    response = view(request, uuid=requester.uuid)
    return response


@pytest.mark.django_db
class TestPostUser:
    def test_admin_create_request_succeeds(self):  #
        requester = SeedUser.get_user(garry_name)
        client = APIClient()
        client.force_authenticate(user=requester)

        target_user = SeedUser.get_user(valerie_name)
        url = reverse("user-detail", args=[target_user.uuid])
        data = {
            "username": "createuser",
            "last_name": "created",
            "gmail": "create@example.com",
            "password": "password",
            "time_zone": "America/Los_Angeles",
        }
        print(user_create_fields[global_admin])
        response = client.post(url, data, format="json")
        print(response.json())
        assert response.status_code == status.HTTP_200_OK

    def test_admin_cannot_create_created_at(self):
        requester = SeedUser.get_user(garry_name)
        client = APIClient()
        client.force_authenticate(user=requester)

        target_user = SeedUser.get_user(valerie_name)
        url = reverse("user-detail", args=[target_user.uuid])
        data = {
            "created_at": "2022-01-01T00:00:00Z",
        }
        response = client.post(url, data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "created_at" in response.json()[0]

    def validate_fields_createable(self):
        PermissionUtil.validate_fields_postable(
            SeedUser.get_user(garry_name),
            SeedUser.get_user(valerie_name),
            ["first_name", "last_name", "gmail"],
        )

    def test_created_at_not_createable(self):
        with pytest.raises(ValidationError):
            PermissionUtil.validate_fields_postable(
                SeedUser.get_user(garry_name),
                SeedUser.get_user(valerie_name),
                ["created_at"],
            )

    def test_project_lead_can_create_name(self):
        PermissionUtil.validate_fields_postable(
            SeedUser.get_user(wanda_name),
            SeedUser.get_user(wally_name),
            ["first_name", "last_name"],
        )

    def test_project_lead_cannot_create_current_title(self):
        with pytest.raises(ValidationError):
            PermissionUtil.validate_fields_postable(
                SeedUser.get_user(wanda_name),
                SeedUser.get_user(wally_name),
                ["current_title"],
            )

    def test_cannot_create_first_name_for_member_of_other_project(self):
        with pytest.raises(PermissionError):
            PermissionUtil.validate_fields_postable(
                SeedUser.get_user(wanda_name),
                SeedUser.get_user(patti_name),
                ["first_name"],
            )

    def test_team_member_cannot_create_first_name_for_member_of_same_project(self):
        with pytest.raises(PermissionError):
            PermissionUtil.validate_fields_postable(
                SeedUser.get_user(wally_name),
                SeedUser.get_user(winona_name),
                ["first_name"],
            )

    def test_multi_project_requester_can_create_first_name_of_member_if_requester_is_project_leader(
        self,
    ):
        PermissionUtil.validate_fields_postable(
            SeedUser.get_user(zani_name), SeedUser.get_user(wally_name), ["first_name"]
        )

    def test_multi_project_user_cannot_create_first_name_of_member_if_reqiester_is_project_member(
        self,
    ):
        with pytest.raises(PermissionError):
            PermissionUtil.validate_fields_postable(
                SeedUser.get_user(zani_name),
                SeedUser.get_user(patti_name),
                ["first_name"],
            )

    def test_allowable_create_fields_configurable(self):
        """Test that the fields that can be created are configurable.

        This test mocks a PATCH request to skip submitting the request to the server and instead
        calls the view directly with the request.  This is done so that variables used by the
        server can be set to test values.
        """

        user_field_permissions[project_lead] = {
            "last_name": "CRU",
            "gmail": "CRU",
            "username": "CRU",
            "password": "CRU",
            "timezone": "CRU",
        }

        requester = SeedUser.get_user(garry_name)  # global admin
        create_data = {
            "username": "fred",
            "password": "hellothere",
            "last_name": "Smith",
            "gmail": "smith@example.com",
            "time_zone": "America/Los_Angeles",
        }
        target_user = SeedUser.get_user(wally_name)
        derive_cru_fields()
        response = post_request_to_view(requester, target_user, create_data)
        print(response)

        assert response.status_code == status.HTTP_201_CREATED

    def test_not_allowable_create_fields_configurable(self):
        """Test that the fields that are not configured to be created cannot be created.

        See documentation for test_allowable_create_fields_configurable for more information.
        """

        requester = SeedUser.get_user(wanda_name)  # project lead for website
        create_data = {"last_name": "Smith"}
        target_user = SeedUser.get_user(wally_name)
        derive_cru_fields()
        response = post_request_to_view(requester, target_user, create_data)

        assert response.status_code == status.HTTP_200_OK
