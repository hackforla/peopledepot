import hashlib
import hmac
import time

from django.contrib.auth.models import Group
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.test import APITestCase

from core.models import User
from peopledepot.settings import SECRET_API_KEY

secret_url = reverse("secret-api-getusers-list")


class SecretUserViewSetTests(APITestCase):
    def setUp(self):
        # Create a test user
        self.client = APIClient()

    def generate_signature(self, api_key, timestamp):
        # Generate a valid signature
        message = f"{timestamp}{api_key}"
        return hmac.new(
            SECRET_API_KEY.encode("utf-8"), message.encode(), hashlib.sha256
        ).hexdigest()

    def test_access_with_invalid_signature(self):
        response = self.client.get(
            secret_url,
            HTTP_X_API_Key=SECRET_API_KEY,
            HTTP_X_API_Timestamp=str(int(time.time())),
            HTTP_X_API_Signature="invalidsignature",
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_access_with_invalid_timestamp(self):
        invalid_timestamp = str(int(time.time()) - 20)  # Invalid timestamp (too old)
        signature = self.generate_signature(SECRET_API_KEY, invalid_timestamp)
        response = self.client.get(
            secret_url,
            HTTP_X_API_Key=SECRET_API_KEY,
            HTTP_X_API_Timestamp=invalid_timestamp,
            HTTP_X_API_Signature=signature,
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_succeeds_with_valid_signature_without_authentication(self):
        timestamp = str(int(time.time()))
        signature = self.generate_signature(SECRET_API_KEY, timestamp)
        response = self.client.get(
            secret_url,
            HTTP_X_API_Key=SECRET_API_KEY,
            HTTP_X_API_Timestamp=timestamp,
            HTTP_X_API_Signature=signature,
        )
        assert response.status_code == status.HTTP_200_OK
        self.client.force_authenticate(user=None)  # Log out the user

    def test_succeeds_with_valid_signature_and_authentication(self):
        user = User.objects.create_user(username="testuser", password="testpassword")
        self.client.force_authenticate(user=user)
        timestamp = str(int(time.time()))
        signature = self.generate_signature(SECRET_API_KEY, timestamp)
        response = self.client.get(
            secret_url,
            HTTP_X_API_Key=SECRET_API_KEY,
            HTTP_X_API_Timestamp=timestamp,
            HTTP_X_API_Signature=signature,
        )
        assert response.status_code == status.HTTP_200_OK
        self.client.force_authenticate(user=None)  # Log out the user

    def test_list_users(self):
        user = User.objects.create_user(username="testuser", password="testpassword")
        group = Group.objects.create(name="testgroup")
        group2 = Group.objects.create(name="testgroup2")
        # third group created to confirm len(user.groups) does not include group3
        Group.objects.create(name="testgroup3")
        user.groups.add(group)
        user.groups.add(group2)

        timestamp = str(int(time.time()))
        signature = self.generate_signature(SECRET_API_KEY, timestamp)
        response = self.client.get(
            secret_url,
            HTTP_X_API_Key=SECRET_API_KEY,
            HTTP_X_API_Timestamp=timestamp,
            HTTP_X_API_Signature=signature,
        )
        assert response.status_code == status.HTTP_200_OK

        group_count = len(response.data[0]["groups"])
        self.assertEqual(group_count, 2)
