from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
import pytest
from rest_framework.test import APIClient


User = get_user_model()
url = reverse("user_app_kb")

@pytest.mark.django_db
@pytest.mark.user_app_kb_data_setup # noqa: PYTEST_MARK_UNKNOWN
class UserAppKbApiTestCase(APITestCase):
    # populated by load_user_app_kb_data.py
    user = None
    other_user = None
    kb_client = None
    kb_user = None
    token = ""

    def setUp(self):
        self.kb_client = APIClient()
        self.kb_client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")


    def test_access_without_permission(self):
        # Remove permission
        self.user.groups.clear()
        response = self.kb_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_access_with_permission(self):
        response = self.kb_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filter_by_email(self):
        response = self.kb_client.get(url, {"email": "testuser@example.com"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["email"], "testuser@example.com")

    def test_filter_by_username(self):
        response = self.kb_client.get(url, {"username": "kbuser1"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["username"], "kbuser1")

    def test_filter_with_email_for_user_without_kbuser(self):
        response = self.kb_client.get(url, {"email": "otheruser@example.com"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_no_filters(self):
        response = self.kb_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Ensure it returns all users

    def test_correct_fields_in_response(self):
        response = self.kb_client.get(url, {"email": "testuser@example.com"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("uuid", response.data[0])
        self.assertIn("username", response.data[0])
        self.assertNotIn("phone", response.data[0])  # Ensure excluded fields are not present

    def test_access_without_authentication(self):
        self.kb_client.logout()
        response = self.kb_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
