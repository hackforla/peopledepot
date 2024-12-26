from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import Permission, Group
from rest_framework_jwt.settings import api_settings
import pytest

User = get_user_model()

@pytest.mark.django_db("user_app_kb_data_setup")
class BasicUserViewSetTestCase(APITestCase):
    # populated by load_user_app_kb_data.py
    user = None
    other_user = None
    kb_client = None
    kb_user = None

    def setUp(self):

        self.url = reverse("user_app_kb")  # Replace with the actual name of your viewset's list route

    @pytest.mark.django_db("user_app_kb_data_setup")
    def test_access_without_permission(self):
        # Remove permission
        self.user.groups.clear()
        response = self.kb_client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_access_with_permission(self):
        print(f"Parent classes of BasicUserViewSetTestCase: {BasicUserViewSetTestCase.__bases__}")

        # print("debug2", f"NodeKeywords: {self}")
        response = self.kb_client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filter_by_email(self):
        response = self.kb_client.get(self.url, {"email": "testuser@example.com"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["email"], "testuser@example.com")

    def test_filter_by_username(self):
        response = self.kb_client.get(self.url, {"username": "kbuser1"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["username"], "kbuser1")

    def test_filter_with_email_for_user_without_kbuser(self):
        response = self.kb_client.get(self.url, {"email": "otheruser@example.com"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_no_filters(self):
        response = self.kb_client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print("response", response.data, len(response.data))
        self.assertEqual(len(response.data), 2)  # Ensure it returns all users

    def test_correct_fields_in_response(self):
        response = self.kb_client.get(self.url, {"email": "testuser@example.com"})
        print("response", response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("uuid", response.data[0])
        self.assertIn("username", response.data[0])
        self.assertNotIn("phone", response.data[0])  # Ensure excluded fields are not present

    def test_access_without_authentication(self):
        self.kb_client.logout()
        response = self.kb_client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
