import pytest
from django.urls import reverse
from rest_framework import status

from core.api.serializers import ProgramAreaSerializer
from core.models import ProgramArea
from core.models import UserPermission

pytestmark = pytest.mark.django_db

USER_PERMISSIONS_URL = reverse("user-permission-list")
PROJECTS_URL = reverse("project-list")
ME_URL = reverse("my_profile")
USER_STATUS_TYPES_URL = reverse("user-status-type-list")
USERS_URL = reverse("user-list")
EVENTS_URL = reverse("event-list")
PRACTICE_AREA_URL = reverse("practice-area-list")
FAQS_URL = reverse("faq-list")
FAQS_VIEWED_URL = reverse("faq-viewed-list")
AFFILIATE_URL = reverse("affiliate-list")
LOCATION_URL = reverse("location-list")
PROGRAM_AREA_URL = reverse("program-area-list")
SKILL_URL = reverse("skill-list")
STACK_ELEMENT_URL = reverse("stack-element-list")
PERMISSION_TYPE = reverse("permission-type-list")
STACK_ELEMENT_TYPE_URL = reverse("stack-element-type-list")
SDG_URL = reverse("sdg-list")
AFFILIATION_URL = reverse("affiliation-list")
CHECK_TYPE_URL = reverse("check-type-list")
SOC_MAJOR_URL = reverse("soc-major-list")
URL_TYPE_URL = reverse("url-type-list")
USER_STATUS_TYPES_URL = reverse("user-status-type-list")


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


def test_create_stack_element(auth_client, stack_element_type):
    payload = {
        "name": "Test StackElement",
        "description": "StackElement description",
        "url": "http://www.testurl.org",
        "logo": "http://www.logourl.com",
        "active": True,
        "element_type": stack_element_type.pk,
    }
    res = auth_client.post(STACK_ELEMENT_URL, payload)
    assert res.status_code == status.HTTP_201_CREATED
    assert res.data["name"] == payload["name"]


def test_create_permission_type(auth_client):
    payload = {"name": "newRecord", "description": "Can CRUD anything"}
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


def test_get_user_permissions(user_superuser_admin, auth_client):
    auth_client.force_authenticate(user=user_superuser_admin)
    permission_count = UserPermission.objects.count()
    res = auth_client.get(USER_PERMISSIONS_URL)
    assert len(res.data) == permission_count
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


def test_create_check_type(auth_client):
    payload = {
        "name": "This is a test check_type",
        "description": "This is a test description",
    }
    res = auth_client.post(CHECK_TYPE_URL, payload)
    assert res.status_code == status.HTTP_201_CREATED
    assert res.data["name"] == payload["name"]


def test_create_soc_major(auth_client):
    """Test that we can create a soc major"""

    payload = {
        "occ_code": "33-3333",
        "title": "Test marketing and sales",
    }
    res = auth_client.post(SOC_MAJOR_URL, payload)
    assert res.status_code == status.HTTP_201_CREATED
    assert res.data["title"] == payload["title"]


def test_project_sdg_xref(auth_client, project, sdg, sdg1):
    def get_object(objects, target_uuid):
        for obj in objects:
            if str(obj["uuid"]) == str(target_uuid):
                return obj
        return None

    project.sdgs.add(sdg)
    project.sdgs.add(sdg1)
    proj_res = auth_client.get(PROJECTS_URL)
    test_proj = get_object(proj_res.data, project.uuid)
    assert test_proj is not None
    assert len(test_proj["sdgs"]) == 2
    assert sdg.name in test_proj["sdgs"]
    assert sdg1.name in test_proj["sdgs"]

    sdg_res = auth_client.get(SDG_URL)
    test_sdg = get_object(sdg_res.data, sdg.uuid)
    assert test_sdg is not None
    assert len(test_sdg["projects"]) == 1
    assert project.name in test_sdg["projects"]


def test_create_url_type(auth_client):
    """Test that we can create a url type"""

    payload = {
        "name": "This is a test url type name",
        "description": "this is a test url type description",
    }
    res = auth_client.post(URL_TYPE_URL, payload)
    assert res.status_code == status.HTTP_201_CREATED
    assert res.data["name"] == payload["name"]
    assert res.data["description"] == payload["description"]


def test_create_user_status_type(auth_client):
    payload = {
        "name": "Test User Status Type",
        "description": "Test User Status Type description",
    }
    res = auth_client.post(USER_STATUS_TYPES_URL, payload)
    assert res.status_code == status.HTTP_201_CREATED
    assert res.data["name"] == payload["name"]
