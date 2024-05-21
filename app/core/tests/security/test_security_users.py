from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from .data_loader import UserData

class TestUser(TestCase):
    def testSetup(self):
        UserData.initialize_data()
        assert UserData.data_loaded == True
        
    def test_get_all_users(self):
        test_data = [
            ("Wanda", ["Wanda", "Winona", "Wally"], "Wanda and Winona users"),
            ("Winona", ["Wanda", "Winona", "Wally"], "Wanda and Winona users"),
            # Add more test cases as needed
        ]
        
        for logged_in_user_name, valid_user_names, description in test_data:
            with self.subTest(logged_in_user_name=logged_in_user_name, valid_user_names=valid_user_names, description=description):
                logged_in_user = UserData.get_user(logged_in_user_name)
                client = APIClient()
                client.force_authenticate(user=logged_in_user)
                url = reverse('user-list')  # Update this to your actual URL name
                response = client.get(url)
                self.assertTrue(logged_in_user is not None)
                self.assertEqual(response.status_code, 200, f"Expected status code 200, got {response.status_code}. Response: {response.data}")

   
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

