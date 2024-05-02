import pytest
from rest_framework.test import APIClient

from ..models import Event
from ..models import Faq
from ..models import FaqViewed
from ..models import Location
from ..models import Permission
from ..models import PermissionType
from ..models import PracticeArea
from ..models import ProgramArea
from ..models import Project
from ..models import Sdg
from ..models import Skill
from ..models import SponsorPartner
from ..models import StackElementType
from ..models import Technology
from ..models import User


@pytest.fixture
def user(django_user_model):
    return django_user_model.objects.create_user(
        username="TestUser",
        email="testuser@email.com",
        password="testpass",
    )


@pytest.fixture
def user2(django_user_model):
    return django_user_model.objects.create_user(
        username="TestUser2",
        email="testuser2@email.com",
        password="testpass",
    )


@pytest.fixture
def admin(django_user_model):
    return django_user_model.objects.create_user(
        is_staff=True,
        username="TestAdminUser",
        email="testadmin@email.com",
        password="testadmin",
    )


@pytest.fixture
def project():
    return Project.objects.create(name="Test Project")


@pytest.fixture
def event(project):
    return Event.objects.create(name="Test Event", project=project)


@pytest.fixture
def practice_area():
    return PracticeArea.objects.create(
        name="Test Practice Area", description="Test Description"
    )


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def auth_client(user, client):
    client.force_authenticate(user=user)
    return client


@pytest.fixture
def auth_client2(user2, client):
    client.force_authenticate(user=user2)
    return client


@pytest.fixture
def admin_client(admin, client):
    client.force_authenticate(user=admin)
    return client


@pytest.fixture
def sponsor_partner():
    return SponsorPartner.objects.create(partner_name="Test Sponsor Partner")


@pytest.fixture
def faq():
    return Faq.objects.create(question="Test Faq")


@pytest.fixture
def faq_viewed(faq):
    return FaqViewed.objects.create(faq=faq)


@pytest.fixture
def location():
    return Location.objects.create(name="Test Hack for L.A. HQ")


@pytest.fixture
def program_area():
    return ProgramArea.objects.create(name="Test Program Area")


@pytest.fixture
def skill():
    return Skill.objects.create(name="Test Skill")


@pytest.fixture
def technology():
    return Technology.objects.create(name="Test Technology")


@pytest.fixture
def permission_type1():
    return PermissionType.objects.create(name="Test Permission Type", description="")


@pytest.fixture
def permission_type2():
    return PermissionType.objects.create(
        name="Test Permission Type", description="A permission type description"
    )


@pytest.fixture
def stack_element_type():
    return StackElementType.objects.create(name="Test Stack Element Type")


@pytest.fixture
def sdg():
    return Sdg.objects.create(name="Test SDG name")


@pytest.fixture
def field_level_user():
    return [
        User.objects.create(
            uuid=1,
            name_first="Admin",
            phone="555-222-3333",
            texting_ok=True,
            preferred_email="admin@something908.com"
        ),
        User.objects.create(
            uuid=2,
            name_first="Sarah",
            phone="555-235-8989",
            texting_ok=True,
            preferred_email="sarah@something908.com"
        ),
        User.objects.create(
            uuid=3,
            name_first="Bob",
            phone="555-456-7890",
            texting_ok=False,
            preferred_email="bob@something908.com"
        ),
        User.objects.create(
            uuid=4,
            name_first="Alice",
            phone="555-765-4321",
            texting_ok=True,
            preferred_email="alice@something908.com"
        ),
        User.objects.create(
            uuid=5,
            name_first="Joe",
            phone="555-468-5656",
            texting_ok=False,
            preferred_email="joe@something908.com"
        ),
        User.objects.create(
            uuid=6,
            name_first="snoop",
            phone="555-555-5656",
            texting_ok=False,
            preferred_email="snoop@something908.com"
        ),
        User.objects.create(
            uuid=7,
            name_first="Ralph",
            phone="555-555-8888",
            texting_ok=True,
            preferred_email="ralph@something908.com"
        ),
        User.objects.create(
            uuid=8,
            name_first="Claire",
            phone="555-555-6666",
            texting_ok=True,
            preferred_email="claire@something908.com"
        ),
        User.objects.create(
            uuid=9,
            name_first="Mary",
            phone="555-555-2222",
            texting_ok=False,
            preferred_email="mary@something908.com"
        ),
    ]

@pytest.fixture
def field_level_permission():
    return [
        Permission.objects.create(
            user_id=1,
            project_id=1,
            practice_area_id=1,
            permission_type_id=1,
            granted="2023-12-01"
        ),
        Permission.objects.create(
            user_id=2,
            project_id=1,
            practice_area_id=2,
            permission_type_id=2,
            granted="2023-12-01"
        ),
        Permission.objects.create(
            user_id=2,
            project_id=2,
            practice_area_id=2,
            permission_type_id=2,
            granted="2024-01-01"
        ),
        Permission.objects.create(
            user_id=3,
            project_id=1,
            practice_area_id=3,
            permission_type_id=3,
            granted="2023-12-01"
        ),
        Permission.objects.create(
            user_id=4,
            project_id=1,
            practice_area_id=3,
            permission_type_id=3,
            granted="2023-12-30"
        ),
        Permission.objects.create(
            user_id=4,
            project_id=1,
            practice_area_id=3,
            permission_type_id=4,
            granted="2023-12-01",
            ended="2023-12-30"
        ),
        Permission.objects.create(
            user_id=4,
            practice_area_id=3,
            permission_type_id=5,
            granted="2023-11-01",
            ended="2023-12-01"
        ),
        Permission.objects.create(
            user_id=6,
            project_id=1,
            practice_area_id=3,
            permission_type_id=4,
            granted="2023-12-01",
        ),
        Permission.objects.create(
            user_id=5,
            practice_area_id=3,
            permission_type_id=5,
            granted="2023-12-01",
        ),
        Permission.objects.create(
            user_id=7,
            project_id=2,
            practice_area_id=3,
            permission_type_id=4,
            granted="2023-12-01",
        ),
        Permission.objects.create(
            user_id=8,
            project_id=1,
            practice_area_id=3,
            permission_type_id=3,
            granted="2023-12-01",
        ),
        Permission.objects.create(
            user_id=9,
            project_id=1,
            practice_area_id=4,
            permission_type_id=4,
            granted="2023-12-01",
        ),
    ]

@pytest.fixture
def field_level_permission_type():
    return [
        PermissionType.objects.create(
            uuid=1,
            name="adminBrigade"
        ),
        PermissionType.objects.create(
            uuid=2,
            name="adminProject"
        ),
        PermissionType.objects.create(
            uuid=3,
            name="practiceLeadProject"
        ),
        PermissionType.objects.create(
            uuid=4,
            name="memberProject"
        ),
        PermissionType.objects.create(
            uuid=5,
            name="memberGeneral"
        )
    ]

@pytest.fixture
def field_level_practice_area():
    return [
        PracticeArea.objects.create(
            uuid=1,
            name="admin"
        ),
        PracticeArea.objects.create(
            uuid=2,
            name="pm"
        ),
        PracticeArea.objects.create(
            uuid=3,
            name="research"
        ),
        PracticeArea.objects.create(
            uuid=4,
            name="design"
        )
    ]

@pytest.fixture
def field_level_project():
    return [
        Project.objects.create(
            uuid=1,
            name="website"
        ),
        Project.objects.create(
            uuid=2,
            name="people depot"
        ),
    ]