import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from core.tests.security.data_loader import UserData
from .seed_constants import (wally_name, wanda_name, winona_name, zani_name, patti_name, patrick_name, paul_name, garry_name, valerie_name)

@pytest.mark.usefixtures("user_tests_initialization")
@pytest.mark.django_db
class TestUser:
    
    @pytest.mark.django_db    
    def test_project_permission_assignment(self):
        UserData.initialize_data()
        logged_in_user_name = wally_name
        logged_in_user = UserData.get_user(logged_in_user_name)
        client = APIClient()
        client.force_authenticate(user=logged_in_user)
        url = reverse('user-list')  # Update this to your actual URL name
        response = client.get(url)
        print(logged_in_user)
        print(response.__dict__)
        
    @pytest.mark.django_db
    def test_get_all_users(self):
        test_data = [
            ("Wanda", ["Wanda", "Winona", "Wally"], "Wanda and Winona users"),
            ("Winona", ["Wanda", "Winona", "Wally"], "Wanda and Winona users"),
            # Add more test cases as needed
        ]
        
        UserData.initialize_data()

        client = APIClient()
        logged_in_user_name = wally_name
        logged_in_user = UserData.get_user(logged_in_user_name)
        client.force_authenticate(user=logged_in_user)
        url = reverse('user-list')  # Update this to your actual URL name
        response = client.get(url)
        assert logged_in_user is not None
        assert response.status_code==200, f"Expected status code 200, got {response.status_code}. Response: {response.data}"

   
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

