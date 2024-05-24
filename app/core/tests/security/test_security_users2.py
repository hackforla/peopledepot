from core.tests.test_api import CREATE_USER_PAYLOAD
from rest_framework import status
import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from core.tests.security.data_loader2 import UserData2
from .seed_constants import (wally_name, wanda_name, winona_name, zani_name, patti_name, patrick_name, paul_name, garry_name, valerie_name)
from django.contrib.auth import get_user_model
from core.pd_util import PdUtil
from core.constants import read_fields

def fields_match(first_name, user_data, fields):
    for user in user_data:
        if user["first_name"] == first_name:
            return set(user.keys()) == set(fields)
    return False

user_actions_test_data = [
    (
        "admin_client",
        "post",
        "users_url",
        CREATE_USER_PAYLOAD,
        status.HTTP_201_CREATED,
    ),
    ("admin_client", "get", "users_url", {}, status.HTTP_200_OK),
    (
        "auth_client",
        "post",
        "users_url",
        CREATE_USER_PAYLOAD,
        status.HTTP_201_CREATED,
    ),
    ("auth_client", "get", "users_url", {}, status.HTTP_200_OK),
    (
        "auth_client",
        "patch",
        "user_url",
        {"first_name": "TestUser2"},
        status.HTTP_200_OK,
    ),
    (
        "auth_client",
        "put",
        "user_url",
        CREATE_USER_PAYLOAD,
        status.HTTP_200_OK,
    ),
    ("auth_client", "delete", "user_url", {}, status.HTTP_204_NO_CONTENT),
    (
        "admin_client",
        "patch",
        "user_url",
        {"first_name": "TestUser2"},
        status.HTTP_200_OK,
    ),
    (
        "admin_client",
        "put",
        "user_url",
        CREATE_USER_PAYLOAD,
        status.HTTP_200_OK,
    ),
    ("admin_client", "delete", "user_url", {}, status.HTTP_204_NO_CONTENT),
    (
        "auth_client2",
        "patch",
        "user_url",
        {"first_name": "TestUser2"},
        status.HTTP_200_OK,
    ),
    (
        "auth_client2",
        "put",
        "user_url",
        CREATE_USER_PAYLOAD,
        status.HTTP_200_OK,
    ),
    ("auth_client2", "delete", "user_url", {}, status.HTTP_204_NO_CONTENT),
]


@pytest.mark.django_db
class TestUser:
    
    @classmethod
    def authenticate_user(cls, user_name):
        logged_in_user = UserData2.get_user(user_name)
        client = APIClient()
        client.force_authenticate(user=logged_in_user)
        url = reverse('user-list')  # Update this to your actual URL name
        response = client.get(url)
        return logged_in_user, response
    
    def test_lead_util(self, user_tests_init2):
        assert PdUtil.is_admin(UserData2.garry_user)
        assert not PdUtil.is_admin(UserData2.wanda_user)
        assert PdUtil.can_read_basic(UserData2.wally_user, UserData2.winona_user)
        assert PdUtil.can_read_basic(UserData2.wally_user, UserData2.wanda_user)
        assert not PdUtil.can_read_basic(UserData2.wally_user, UserData2.paul_user)
        assert not PdUtil.can_read_basic(UserData2.wally_user, UserData2.garry_user)
        assert PdUtil.can_read_secure(UserData2.wanda_user, UserData2.wally_user)
        assert not PdUtil.can_read_secure(UserData2.wally_user, UserData2.wanda_user)
        assert not PdUtil.can_read_secure(UserData2.wanda_user, UserData2.paul_user)


    # def test_global_admin(self, user_tests_init):
    #     logged_in_user, response = self.authenticate_user(garry_name)
    #     assert logged_in_user is not None
    #     assert response.status_code == 200
    #     assert get_user_model().objects.count() > 0
    #     assert len(response.json()) == len(UserData2.users)
        
    # def test_multi_project_user(self, user_tests_init):
    #     logged_in_user, response = self.authenticate_user(zani_name)
    #     assert logged_in_user is not None
    #     assert response.status_code == 200
    #     print("debug multi json", response.json())
    #     for user in response.json():
    #         print("debug multi project user", user["first_name"])
    #     assert len(response.json()) == 7
    #     assert fields_match(wanda_name, response.json(), read_fields["user"]["secure"] )
    #     assert fields_match(paul_name, response.json(), read_fields["user"]["basic"] )


    # def test_project_lead(self, user_tests_init):
    #     logged_in_user, response = self.authenticate_user(wanda_name)
    #     assert logged_in_user is not None
    #     assert response.status_code == 200
    #     assert len(response.json()) == 4
    #     assert fields_match(winona_name, response.json(), read_fields["user"]["secure"] )
        
 
    # def test_project_team_member(self, user_tests_init):
    #     logged_in_user, response = self.authenticate_user(wally_name)
    #     assert logged_in_user is not None
    #     assert response.status_code == 200
    #     print("debug json", response.json())
    #     assert fields_match(winona_name, response.json(), read_fields["user"]["basic"] )
    #     assert fields_match(wanda_name, response.json(), read_fields["user"]["basic"] )
    #     assert len(response.json()) == 4

    # def test_no_project(self, user_tests_init):
    #     logged_in_user, response = self.authenticate_user(valerie_name)
    #     assert logged_in_user is not None
    #     assert response.status_code == 200
    #     assert len(response.json()) == 0

