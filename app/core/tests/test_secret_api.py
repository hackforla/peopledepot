import datetime

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_api_key.models import APIKey

secret_url = reverse("secret-api-getusers-list")


class SecretUserViewSetTests(APITestCase):
    def test_succeeds(self):
        _, api_key = APIKey.objects.create_key(name="test")
        response = self.client.get(
            secret_url,
            HTTP_X_API_KEY=api_key,  # Uppercase X-API-KEY
            Content_Type="application/json",
        )
        assert response.status_code == status.HTTP_200_OK

    def test_expired_fails(self):
        expired_date = datetime.datetime.now() - datetime.timedelta(days=2)
        _, api_key = APIKey.objects.create_key(name="test", expiry_date=expired_date)
        response = self.client.get(
            secret_url,
            HTTP_X_API_KEY=api_key,  # Uppercase X-API-KEY
            Content_Type="application/json",
        )
        assert response.status_code == status.HTTP_401UNAUTHORIZED
