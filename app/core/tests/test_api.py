import json

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

ME_URL = reverse("my_profile")
USERS_URL = reverse("user-list")


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserAPITests(TestCase):
    pass

    def test_list_users_not_allowed(self):
        res = self.client.get(USERS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserAPITests(TestCase):
    def setUp(self):
        self.user = create_user(username="TestUser", password="testpass")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_profile(self):
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["username"], self.user.username)

    def test_list_users_success(self):
        res = self.client.get(USERS_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        data = json.loads(res.content)
        self.assertEqual(len(data), 1)
