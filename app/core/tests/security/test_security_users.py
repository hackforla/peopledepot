import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from core.tests.security.data_loader import UserData
from .seed_constants import (wally_name, wanda_name, winona_name, zani_name, patti_name, patrick_name, paul_name, garry_name, valerie_name)
from django.contrib.auth import get_user_model
from core.pd_util import PdUtil

@pytest.mark.django_db
class TestUser:
    
    @classmethod
    def authenticate_user(cls, user_name):
        logged_in_user = UserData.get_user(user_name)
        client = APIClient()
        client.force_authenticate(user=logged_in_user)
        url = reverse('user-list')  # Update this to your actual URL name
        response = client.get(url)
        return logged_in_user, response
    
    def test_lead_util(self, user_tests_init):
        assert PdUtil.is_admin(UserData.garry_user)
        assert not PdUtil.is_admin(UserData.wanda_user)
        assert PdUtil.can_read_basic(UserData.wally_user, UserData.winona_user)
        assert PdUtil.can_read_basic(UserData.wally_user, UserData.wanda_user)
        assert not PdUtil.can_read_basic(UserData.wally_user, UserData.paul_user)
        assert not PdUtil.can_read_basic(UserData.wally_user, UserData.garry_user)

    def test_global_admin(self, user_tests_init):
        logged_in_user, response = self.authenticate_user(garry_name)
        assert logged_in_user is not None
        assert response.status_code == 200
        assert get_user_model().objects.count() > 0
        assert len(response.json()) == len(UserData.users)


    def test_project_lead(self, user_tests_init):
        logged_in_user, response = self.authenticate_user(wanda_name)
        assert logged_in_user is not None
        assert response.status_code == 200
        assert len(response.json()) == 4
        
 
    def test_project_team_member(self, user_tests_init):
        logged_in_user, response = self.authenticate_user(wally_name)
        assert logged_in_user is not None
        assert response.status_code == 200
        assert len(response.json()) == 4

    def test_no_project(self, user_tests_init):
        logged_in_user, response = self.authenticate_user(valerie_name)
        assert logged_in_user is not None
        assert response.status_code == 200
        assert len(response.json()) == 0

