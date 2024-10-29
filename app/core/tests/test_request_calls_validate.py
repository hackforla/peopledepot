import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


from core.api.permission_check import FieldPermissionCheck
from core.models import User
from core.tests.utils.seed_constants import garry_name
from core.tests.utils.seed_constants import valerie_name

from core.tests.utils.seed_user import SeedUser
from unittest.mock import patch

count_website_members = 4
count_people_depot_members = 3
count_members_either = 6


@pytest.mark.django_db
@pytest.mark.load_user_data_required  # see load_user_data_required in conftest.py
class TestRequestCallsValidate:

    @patch.object(FieldPermissionCheck, "validate_user_related_request")
    def test_patch_request_calls_validate_request(self, mock_validate_user_related_request):
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
        client.patch(url, data, format="json")
        __args__, kwargs = mock_validate_user_related_request.call_args
        request_received = kwargs.get("request")
        target_user_received = kwargs.get("target_user")
        assert request_received.data == data
        assert request_received.user == requester
        assert request_received.method == "PATCH"
        assert target_user_received == target_user

    @patch.object(FieldPermissionCheck, "validate_user_related_request")
    def test_post_request_calls_validate_request(
        self, mock_validate_user_related_request
    ):
        """Test that the patch requests succeeds when the requester is an admin."""
        requester = SeedUser.get_user(garry_name)
        client = APIClient()
        client.force_authenticate(user=requester)

        url = reverse("user-list")
        data = {
            "last_name": "Updated",
            "gmail": "update@example.com",
        }
        
        client.post(url, data, format="json")
        __args__, kwargs = mock_validate_user_related_request.call_args
        request_received = kwargs.get("request")
        target_user_received = kwargs.get("target_user")
        assert request_received.data == data
        assert request_received.user == requester
        assert request_received.method == "POST"
        assert target_user_received == None

    