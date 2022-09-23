import pytest
from django.urls import reverse
from rest_framework import status

from core.api.serializers import UserSerializer

pytestmark = pytest.mark.django_db

ME_URL = reverse("my_profile")
USERS_URL = reverse("user-list")
RECURRING_EVENTS_URL = reverse("recurring-event-list")
FAQ_URL = reverse("faq-list")


def create_user(django_user_model, **params):
    return django_user_model.objects.create_user(**params)


def test_list_users_fail(client):
    res = client.get(USERS_URL)

    assert res.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_profile(auth_client):
    res = auth_client.get(ME_URL)

    assert res.status_code == status.HTTP_200_OK
    assert res.data["username"] == "TestUser"


def test_get_users(auth_client, django_user_model):
    create_user(django_user_model, username="TestUser2", password="testpass")
    create_user(django_user_model, username="TestUser3", password="testpass")

    res = auth_client.get(USERS_URL)

    assert res.status_code == status.HTTP_200_OK
    assert len(res.data) == 3

    users = django_user_model.objects.all().order_by("created_at")
    serializer = UserSerializer(users, many=True)
    assert res.data == serializer.data


def test_get_single_user(auth_client, user):
    res = auth_client.get(f"{USERS_URL}?email={user.email}")
    assert res.status_code == status.HTTP_200_OK

    res = auth_client.get(f"{USERS_URL}?username={user.username}")
    assert res.status_code == status.HTTP_200_OK


def test_create_user_as_user(auth_client):
    payload = {"username": "TestUser2", "password": "testpass"}
    res = auth_client.post(USERS_URL, payload)
    assert res.status_code == status.HTTP_403_FORBIDDEN


def test_create_user_as_admin(admin_client):
    payload = {
        "username": "TestUserAPI",
        "password": "testpass",
        # time_zone is required because django_timezone_field doesn't yet support the blank string
        "time_zone": "America/Los_Angeles",
    }
    res = admin_client.post(USERS_URL, payload)
    assert res.status_code == status.HTTP_201_CREATED


def test_create_recurring_event(admin_client, project):

    payload = {
        "name": "Weekly team meeting",
        "start_time": "18:00:00",
        "duration_in_min": 60,
        "video_conference_url": "https://zoom.com/link",
        "additional_info": "",
        "project": project.uuid,
    }
    res = admin_client.post(RECURRING_EVENTS_URL, payload)
    assert res.status_code == status.HTTP_201_CREATED


def test_create_faq(admin_client):

    payload = {
        "question": "How do I work on an issue",
        "answer": "See CONTRIBUTING.md",
        "tool_tip_name": "How to work on an issue",
    }
    res = admin_client.post(FAQ_URL, payload)
    assert res.status_code == status.HTTP_201_CREATED

    res = admin_client.get(FAQ_URL, payload)
    assert res.status_code == status.HTTP_200_OK
