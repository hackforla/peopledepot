import pytest
from rest_framework.test import APIClient

from .security.data_loader2 import UserData2
from ..models import Affiliate
from ..models import Affiliation
from ..models import Event
from ..models import Faq
from ..models import FaqViewed
from ..models import Location
from ..models import PermissionType
from ..models import PracticeArea
from ..models import ProgramArea
from ..models import Project
from ..models import Sdg
from ..models import Skill
from ..models import StackElementType
from ..models import Technology

    
@pytest.fixture
def user_tests_init2():
    print("User tests initialization2")
    UserData2.initialize_data()


@pytest.fixture
@pytest.mark.django_db
def init_foo():
    print("Init foo")
    UserData.initialize_data()

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
def affiliate():
    return Affiliate.objects.create(partner_name="Test Affiliate")


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
def affiliation1(project, affiliate):
    return Affiliation.objects.create(
        is_sponsor=True, is_partner=False, project=project, affiliate=affiliate
    )


@pytest.fixture
def affiliation2(project, affiliate):
    return Affiliation.objects.create(
        is_sponsor=False, is_partner=True, project=project, affiliate=affiliate
    )


@pytest.fixture
def affiliation3(project, affiliate):
    return Affiliation.objects.create(
        is_sponsor=True, is_partner=True, project=project, affiliate=affiliate
    )


@pytest.fixture
def affiliation4(project, affiliate):
    return Affiliation.objects.create(
        is_sponsor=False, is_partner=False, project=project, affiliate=affiliate
    )
