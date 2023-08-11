import pytest
from django.urls import reverse
from rest_framework import status

from core.api.serializers import UserSerializer

pytestmark = pytest.mark.django_db

ME_URL = reverse("my_profile")
USERS_URL = reverse("user-list")
RECURRING_EVENTS_URL = reverse("recurring-event-list")
PRACTICE_AREA_URL = reverse("practice-area-list")
FAQS_URL = reverse("faq-list")
FAQS_VIEWED_URL = reverse("faq-viewed-list")
SPONSOR_PARTNERS_URL = reverse("sponsor-partner-list")
LOCATION_URL = reverse("location-list")
PROGRAM_AREA_URL = reverse("program-area-list")
SKILL_URL = reverse("skill-list")
TECHNOLOGY_URL = reverse("technology-list")
LANGUAGES_URL = reverse("language-list")


CREATE_USER_PAYLOAD = {
    "username": "TestUserAPI",
    "password": "testpass",
    # time_zone is required because django_timezone_field doesn't yet support the blank string
    "time_zone": "America/Los_Angeles",
}


@pytest.fixture
def users_url():
    return reverse("user-list")


@pytest.fixture
def user_url(user):
    return reverse("user-detail", args=[user.uuid])


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


user_actions_test_data = [
    (
        "admin_client",
        "post",
        "users_url",
        CREATE_USER_PAYLOAD,
        status.HTTP_201_CREATED,
    ),
    ("admin_client", "get", "users_url", {}, status.HTTP_200_OK),
    (
        "auth_client",
        "post",
        "users_url",
        CREATE_USER_PAYLOAD,
        status.HTTP_201_CREATED,
    ),
    ("auth_client", "get", "users_url", {}, status.HTTP_200_OK),
    (
        "auth_client",
        "patch",
        "user_url",
        {"first_name": "TestUser2"},
        status.HTTP_200_OK,
    ),
    (
        "auth_client",
        "put",
        "user_url",
        CREATE_USER_PAYLOAD,
        status.HTTP_200_OK,
    ),
    ("auth_client", "delete", "user_url", {}, status.HTTP_204_NO_CONTENT),
    (
        "admin_client",
        "patch",
        "user_url",
        {"first_name": "TestUser2"},
        status.HTTP_200_OK,
    ),
    (
        "admin_client",
        "put",
        "user_url",
        CREATE_USER_PAYLOAD,
        status.HTTP_200_OK,
    ),
    ("admin_client", "delete", "user_url", {}, status.HTTP_204_NO_CONTENT),
    (
        "auth_client2",
        "patch",
        "user_url",
        {"first_name": "TestUser2"},
        status.HTTP_200_OK,
    ),
    (
        "auth_client2",
        "put",
        "user_url",
        CREATE_USER_PAYLOAD,
        status.HTTP_200_OK,
    ),
    ("auth_client2", "delete", "user_url", {}, status.HTTP_204_NO_CONTENT),
]


@pytest.mark.parametrize(
    ("client_name", "action", "endpoint", "payload", "expected_status"),
    user_actions_test_data,
)
def test_user_actions(client_name, action, endpoint, payload, expected_status, request):
    client = request.getfixturevalue(client_name)
    action_fn = getattr(client, action)
    url = request.getfixturevalue(endpoint)
    res = action_fn(url, payload)
    assert res.status_code == expected_status


def test_create_recurring_event(auth_client, project):
    """Test that we can create a recurring event"""

    payload = {
        "name": "Test Weekly team meeting",
        "start_time": "18:00:00",
        "duration_in_min": 60,
        "video_conference_url": "https://zoom.com/link",
        "additional_info": "Test description",
        "project": project.uuid,
    }
    res = auth_client.post(RECURRING_EVENTS_URL, payload)
    assert res.status_code == status.HTTP_201_CREATED
    assert res.data["name"] == payload["name"]


def test_create_sponsor_partner(auth_client):
    payload = {
        "partner_name": "Test Partner",
        "partner_logo": "http://www.logourl.com",
        "is_active": True,
        "url": "http://www.testurl.org",
        "is_sponsor": True,
    }
    res = auth_client.post(SPONSOR_PARTNERS_URL, payload)
    assert res.status_code == status.HTTP_201_CREATED


def test_create_practice_area(auth_client):
    payload = {
        "name": "Test API for creating practice area",
        "description": "See name.  Description is optional.",
    }
    res = auth_client.post(PRACTICE_AREA_URL, payload)
    assert res.status_code == status.HTTP_201_CREATED
    assert res.data["name"] == payload["name"]


def test_create_faq(auth_client):
    payload = {
        "question": "How do I work on an issue",
        "answer": "See CONTRIBUTING.md",
        "tool_tip_name": "How to work on an issue",
    }
    res = auth_client.post(FAQS_URL, payload)
    assert res.status_code == status.HTTP_201_CREATED
    assert res.data["question"] == payload["question"]


def test_get_faq_viewed(auth_client, faq_viewed):
    """test retrieving faq_viewed"""

    res = auth_client.get(FAQS_VIEWED_URL)

    assert res.data[0]["faq"] == faq_viewed.faq.pk


def test_create_location(auth_client):
    """Test that we can create a location"""

    payload = {
        "name": "Test Hack for L.A. HQ",
        "address_line_1": "123 Hacker Way",
        "address_line_2": "Suite 456",
        "city": "Los Angeles",
        "state": "CA",
        "zip": "90210",
    }
    res = auth_client.post(LOCATION_URL, payload)
    assert res.status_code == status.HTTP_201_CREATED


def test_create_program_area(auth_client):
    """Test that we can create a program area"""

    payload = {
        "name": "Test program area",
        "description": "About program area",
        "image": "http://www.imageurl.com",
    }
    res = auth_client.post(PROGRAM_AREA_URL, payload)
    assert res.status_code == status.HTTP_201_CREATED
    assert res.data["name"] == payload["name"]


def test_create_skill(auth_client):
    """Test that we can create a skill"""

    payload = {
        "name": "Test Skill",
        "description": "Skill Description",
    }
    res = auth_client.post(SKILL_URL, payload)
    assert res.status_code == status.HTTP_201_CREATED
    assert res.data["name"] == payload["name"]


def test_create_technology(auth_client):
    """Test to create a Technology"""
    
    payload = {
        "name": "Test Technology",
        "description": "Technology description",
        "url": "http://www.testurl.org",
        "logo": "http://www.logourl.com",
        "active": True,
    }
    res = auth_client.post(TECHNOLOGY_URL, payload)
    assert res.status_code == status.HTTP_201_CREATED
    assert res.data["name"] == payload["name"]


def test_create_language(auth_client):  # add project_language_xref to params
    """Test to create a language"""

    payload = {
        "name": "Test Language",
        "description": "Test Language Description",
        # "project language": project_language_xref.uuid
    }
    res = auth_client.post(LANGUAGES_URL, payload)
    assert res.status_code == status.HTTP_201_CREATED
    assert res.data["name"] == payload["name"]
