import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from core.api.serializers import ProgramAreaSerializer
from core.api.serializers import UserSerializer
from core.models import ProgramArea
from core.models import User
from core.models import UserPermissions

pytestmark = pytest.mark.django_db

USER_PERMISSIONS_URL = reverse("user-permissions-list")
ME_URL = reverse("my_profile")
USERS_URL = reverse("user-list")
EVENTS_URL = reverse("event-list")
PRACTICE_AREA_URL = reverse("practice-area-list")
FAQS_URL = reverse("faq-list")
FAQS_VIEWED_URL = reverse("faq-viewed-list")
AFFILIATE_URL = reverse("affiliate-list")
LOCATION_URL = reverse("location-list")
PROGRAM_AREA_URL = reverse("program-area-list")
SKILL_URL = reverse("skill-list")
TECHNOLOGY_URL = reverse("technology-list")
PERMISSION_TYPE = reverse("permission-type-list")
STACK_ELEMENT_TYPE_URL = reverse("stack-element-type-list")
SDG_URL = reverse("sdg-list")
AFFILIATION_URL = reverse("affiliation-list")

CREATE_USER_PAYLOAD = {
    "username": "TestUserAPI",
    "password": "testpass",
    # time_zone is required because django_timezone_field doesn't yet support
    # the blank string
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


def test_foo():
    assert True


def test_list_users_fail(client):
    res = client.get(USERS_URL)

    assert res.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_profile(auth_client):
    res = auth_client.get(ME_URL)

    assert res.status_code == status.HTTP_200_OK
    assert res.data["username"] == "TestUser"


def test_get_single_user(auth_client, user):
    res = auth_client.get(f"{USERS_URL}?email={user.email}")
    assert res.status_code == status.HTTP_200_OK

    res = auth_client.get(f"{USERS_URL}?username={user.username}")
    assert res.status_code == status.HTTP_200_OK


def test_create_event(auth_client, project):
    """Test that we can create an event"""

    payload = {
        "name": "Test Weekly team meeting",
        "start_time": "18:00:00",
        "duration_in_min": 60,
        "video_conference_url": "https://zoom.com/link",
        "additional_info": "Test description",
        "project": project.uuid,
        "must_attend": [
            {
                "practice_area": "Professional Development",
                "permission_type": "adminProject",
            },
            {"practice_area": "Development", "permission_type": "practiceLeadProject"},
            {"practice_area": "Design", "permission_type": "practiceLeadJrProject"},
        ],
        "should_attend": [
            {"practice_area": "Development", "permission_type": "memberProject"}
        ],
        "could_attend": [
            {"practice_area": "Design", "permission_type": "memberGeneral"}
        ],
    }
    res = auth_client.post(EVENTS_URL, payload)
    assert res.status_code == status.HTTP_201_CREATED
    assert res.data["name"] == payload["name"]


def test_create_affiliate(auth_client):
    payload = {
        "partner_name": "Test Partner",
        "partner_logo": "http://www.logourl.com",
        "is_active": True,
        "url": "http://www.testurl.org",
        "is_org_sponsor": True,
        "is_org_partner": True,
    }
    res = auth_client.post(AFFILIATE_URL, payload)
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


def test_list_program_area(auth_client):
    """Test that we can list program areas"""

    payload = {
        "name": "Test program area",
        "description": "About program area",
        "image": "http://www.imageurl.com",
    }
    res = auth_client.post(PROGRAM_AREA_URL, payload)

    res = auth_client.get(PROGRAM_AREA_URL)

    program_areas = ProgramArea.objects.all()
    expected_data = ProgramAreaSerializer(program_areas, many=True).data

    assert res.status_code == status.HTTP_200_OK
    assert res.data == expected_data


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


def test_create_permission_type(auth_client):
    payload = {"name": "foobar", "description": "Can CRUD anything", "rank": 1000}
    print("Debug payload", payload)
    res = auth_client.post(PERMISSION_TYPE, payload)
    assert res.status_code == status.HTTP_201_CREATED
    assert res.data["name"] == payload["name"]
    assert res.data["description"] == payload["description"]


def test_create_stack_element_type(auth_client):
    payload = {
        "name": "Test Stack Element Type",
        "description": "Stack Element Type description",
    }
    res = auth_client.post(STACK_ELEMENT_TYPE_URL, payload)
    assert res.status_code == status.HTTP_201_CREATED
    assert res.data["name"] == payload["name"]


def test_get_user_permissions(
    created_user_admin, created_user_permissions, auth_client
):
    auth_client.force_authenticate(user=created_user_admin)
    db_count = UserPermissions.objects.count()
    res = auth_client.get(USER_PERMISSIONS_URL)
    assert len(res.data) == db_count
    assert res.status_code == status.HTTP_200_OK


def test_create_sdg(auth_client):
    payload = {
        "name": "Test SDG name",
        "description": "Test SDG description",
        "image": "https://unsplash.com",
    }
    res = auth_client.post(SDG_URL, payload)
    assert res.status_code == status.HTTP_201_CREATED
    assert res.data["name"] == payload["name"]


def test_create_affiliation(auth_client, project, affiliate):
    payload = {
        "affiliate": affiliate.pk,
        "project": project.pk,
        "ended_at": "2024-01-01 18:00:00",
        "is_sponsor": False,
        "is_partner": True,
    }
    res = auth_client.post(AFFILIATION_URL, payload)
    assert res.status_code == status.HTTP_201_CREATED
    assert res.data["is_sponsor"] == payload["is_sponsor"]
    assert res.data["is_partner"] == payload["is_partner"]
    assert res.data["affiliate"] == payload["affiliate"]
    assert res.data["project"] == payload["project"]
