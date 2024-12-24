from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import Permission, Group
from rest_framework_jwt.settings import api_settings

User = get_user_model()

class BasicUserViewSetTestCase(APITestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username="login-kb-user",
            email="testuser@example.com",
            first_name="Test",
            last_name="User",
        )
        self.user.set_password("password123")
        self.user.save()
        group = Group.objects.get(name="kb_user")
        self.user.groups.add(group)


        # Generate a JWT token for the user
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(self.user)
        self.token = jwt_encode_handler(payload)

        # Set the Authorization header for the client
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

        self.kb_user1 = User.objects.create_user(
            username="kbuser1",
            email="kbuser@example.com",
            first_name="Other",
            last_name="User",
        )
        self.kb_user1.groups.add(group)

        # Create additional users
        self.other_user = User.objects.create_user(
            username="otheruser",
            email="otheruser@example.com",
            first_name="Other",
            last_name="User",
        )

        self.url = reverse("user_app_kb")  # Replace with the actual name of your viewset's list route
        print("debug url", self.url)

    def test_access_without_permission(self):
        # Remove permission
        self.user.groups.clear()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_access_with_permission(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filter_by_email(self):
        response = self.client.get(self.url, {"email": "testuser@example.com"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["email"], "testuser@example.com")

    def test_filter_by_username(self):
        response = self.client.get(self.url, {"username": "kbuser1"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["username"], "kbuser1")

    def test_filter_with_email_for_user_without_kbuser(self):
        response = self.client.get(self.url, {"email": "otheruser@example.com"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_no_filters(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print("response", response.data, len(response.data))
        self.assertEqual(len(response.data), 2)  # Ensure it returns all users

    def test_correct_fields_in_response(self):
        response = self.client.get(self.url, {"email": "testuser@example.com"})
        print("response", response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("uuid", response.data[0])
        self.assertIn("username", response.data[0])
        self.assertNotIn("phone", response.data[0])  # Ensure excluded fields are not present

    def test_access_without_authentication(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
