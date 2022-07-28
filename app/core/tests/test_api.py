from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from core.api.serializers import UserSerializer

ME_URL = reverse("my_profile")
USERS_URL = reverse("user-list")


def create_user(**params):
    return get_user_model().objects.create_user(**params)


def create_admin_user(**params):
    return get_user_model().objects.create_user(is_staff=True, **params)


class PublicUserAPITests(TestCase):
    """Test unauthenticated user API access"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test that authentication is required"""
        res = self.client.get(USERS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserAPITests(TestCase):
    """Test authenticated user API access"""

    def setUp(self):
        self.user = create_user(username="TestUser", password="testpass")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_profile(self):
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["username"], self.user.username)

    def test_retrieve_users(self):
        """Test retrieving a list of users"""
        create_user(username="TestUser2", password="testpass")
        create_user(username="TestUser3", password="testpass")

        res = self.client.get(USERS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 3)

        users = get_user_model().objects.all().order_by("created_at")
        serializer = UserSerializer(users, many=True)
        self.assertEqual(res.data, serializer.data)

    def test_create_user_as_user_should_fail(self):
        content = {
            "username": "TestUserAPI",
            "password": "testpass",
        }
        res = self.client.post(USERS_URL, content)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_user_as_superuser_should_succeed(self):
        self.admin_user = create_admin_user(username="TestUser2", password="testpass")
        self.client.force_authenticate(user=self.admin_user)

        content = {
            "username": "TestUserAPI",
            "password": "testpass",
            # time_zone is required because django_timezone_field doesn't yet support the blank string
            "time_zone": "America/Los_Angeles",
        }
        res = self.client.post(USERS_URL, content)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
