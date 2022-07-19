import json

from django.test import TestCase
from django.urls import reverse

from core.models import User


class UserAPITests(TestCase):
    def setUp(self):
        User.objects.get_or_create(name="TestUser", password="Dogfood1!")

    def test_list(self):
        url = reverse("users:user_object_api")
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEquals(len(data), 1)
