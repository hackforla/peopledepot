import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from core.tests.security.data_loader import UserData
from .seed_constants import (wally_name, wanda_name, winona_name, zani_name, patti_name, patrick_name, paul_name, garry_name, valerie_name)
from django.contrib.auth import get_user_model

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

    def test_global_admin(self, user_tests_init):
        logged_in_user, response = self.authenticate_user(garry_name)
        assert logged_in_user is not None
        assert response.status_code == 200
        assert get_user_model().objects.count() > 0
        assert len(response.json()) == len(UserData.users)


    def test_project_lead(self):
        logged_in_user, response = self.authenticate_user(garry_name)
        assert logged_in_user is not None
        assert response.status_code == 200
        # assert len(response.json()) == 4
        
 
   
# WANDA_USER_DATA = { "first_name": "Wanda", "project_name": WEBSITE_PROJECT,"permission_type_name": PROJECT_LEAD}
# WALLY_USER_DATA = { "first_name": "Wally",  "project_name": WEBSITE_PROJECT,"permission_type_name": PROJECT_TEAM_MEMBER}
# WINONA_USER_DATA = { "first_name": "Winona",  "project_name": WEBSITE_PROJECT,"permission_type_name": PROJECT_TEAM_MEMBER}
# PATRICK_USER_DATA = { "first_name": "Patrick",  "project_name": PEOPLE_DEPOT_PROJECT,"permission_type_name": PROJECT_LEAD}
# PATTI_USER_DATA = { "first_name": "Patti",  "project_name": PEOPLE_DEPOT_PROJECT,"permission_type_name": PROJECT_TEAM_MEMBER}
# PERRY_USER_DATA = { "first_name": "Perry",  "project_name": PEOPLE_DEPOT_PROJECT,"permission_type_name": PROJECT_TEAM_MEMBER}
# GARRY_USER_DATA = { "first_name": "Garry",  "permission_type_name": GLOBAL_ADMIN}
# VALERIE_USER_DATA = { "first_name": "Valerie",  "permission_type_name": VERIFIED_USER}

# ZANI_PEOPLE_DEPOT_DATA = { "first_name": "Zani",  "project_name": PEOPLE_DEPOT_PROJECT,"permission_type_name":PROJECT_LEAD}
# ZANI_WEBSITE_ROLE_ASSIGNMENT_DATA = { "project_name": WEBSITE_PROJECT,"permission_type_name":PROJECT_TEAM_MEMBER}

