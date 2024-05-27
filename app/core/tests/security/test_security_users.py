# Change fields that can be viewed in code to what Bonnie specified
# Change fields that can be viewed in my wiki to what Bonnie specified
# Add more tests for update
# Add print statements to explain what is being tested
# Add tests for the patch API
# Add tests for and implement put (disallow), post, and delete API
# Update my Wiki for put, patch, post, delete
# Add proposals

from core.tests.test_api import CREATE_USER_PAYLOAD
from rest_framework import status
import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from core.permission_util import PermissionUtil
from core.constants import Fields, PermissionValue
from core.tests.utils.seed_data import Seed
from core.tests.utils.seed_user import SeedUser
from core.tests.utils.utils_test import show_test_info

count_website_members = 4
count_people_depot_members = 3
count_members_either = 6

def fields_match(first_name, user_data, fields):
    for user in user_data:
        if user["first_name"] == first_name:
            return set(user.keys()) == set(fields)
    return False


@pytest.mark.django_db
class TestUser:
    
    @classmethod
    def authenticate_user(cls, user_name):
        logged_in_user = SeedUser.get_user(user_name)
        client = APIClient()
        client.force_authenticate(user=logged_in_user)
        url = reverse('user-list')  # Update this to your actual URL name
        response = client.get(url)
        return logged_in_user, response
    
    
    def test_validate_fields_update(self, user_tests_init):
        logged_in_user, response = self.authenticate_user(Seed.garry.first_name)
        assert logged_in_user is not None
        assert response.status_code == 200
        assert get_user_model().objects.count() > 0
        show_test_info(f"Field logic: validate global admin Garry can see Fields.read['user'][global_admin]")
        PermissionUtil.validate_fields(Seed.garry.user, Seed.valerie.user, ["first_name"])
        PermissionUtil.validate_fields(Seed.wanda.user, Seed.wally.user, ["first_name"])
        with pytest.raises(Exception):
            PermissionUtil.validate_fields(Seed.wanda.user, Seed.wally.user, ["bogus_field"])

    def test_can_read_logic(self, user_tests_init):

        print(f"Assert Garry {Seed.garry.user.last_name} is admin")
        assert PermissionUtil.is_admin(Seed.garry.user)        
        print(f"Assert Garry {Seed.wanda.user.last_name} is admin")        
        assert not PermissionUtil.is_admin(Seed.wanda.user)
        assert PermissionUtil.can_read_user_basic(Seed.wally.user, Seed.winona.user)
        assert PermissionUtil.can_read_user_basic(Seed.wally.user, Seed.wanda.user)
        assert not PermissionUtil.can_read_user_basic(Seed.wally.user, Seed.garry.user)
        assert PermissionUtil.can_read_user_secure(Seed.wanda.user, Seed.wally.user)
        assert not PermissionUtil.can_read_user_secure(Seed.wally.user, Seed.wanda.user)


    def test_global_admin(self, user_tests_init):
        logged_in_user, response = self.authenticate_user(Seed.garry.first_name)
        assert logged_in_user is not None
        assert response.status_code == 200
        assert get_user_model().objects.count() > 0
        assert len(response.json()) == len(SeedUser.users)
        
    def test_multi_project_user(self, user_tests_init):
        logged_in_user, response = self.authenticate_user(Seed.zani.first_name)
        print("Debug multi", Seed.zani.first_name, logged_in_user, Seed.zani.user, SeedUser.users    )
        assert logged_in_user is not None
        assert response.status_code == 200
        print("debug multi json", response.json())
        for user in response.json():
            print("debug multi project user", user["first_name"])
        assert len(response.json()) == count_members_either
        assert fields_match(Seed.wanda.first_name, response.json(), Fields.read["user"][PermissionValue.global_admin] )
        assert fields_match(Seed.patrick.first_name, response.json(), Fields.read["user"][PermissionValue.basic] )


    def test_project_lead(self, user_tests_init):
        logged_in_user, response = self.authenticate_user(Seed.wanda.first_name)
        assert logged_in_user is not None
        assert response.status_code == 200
        assert len(response.json()) == count_website_members
        assert fields_match(Seed.winona.first_name, response.json(), Fields.read["user"][PermissionValue.global_admin] )
        
 
    def test_project_team_member(self, user_tests_init):
        logged_in_user, response = self.authenticate_user(Seed.wally.first_name)
        assert logged_in_user is not None
        assert response.status_code == 200
        print("debug json", response.json())
        assert fields_match(Seed.winona.first_name, response.json(), Fields.read["user"][PermissionValue.basic] )
        assert fields_match(Seed.wanda.first_name, response.json(), Fields.read["user"][PermissionValue.basic] )
        assert len(response.json()) == count_website_members

    def test_no_project(self, user_tests_init):
        logged_in_user, response = self.authenticate_user(Seed.valerie.first_name)
        assert logged_in_user is not None
        assert response.status_code == 200
        assert len(response.json()) == 0

