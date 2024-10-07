import pytest
from rest_framework.test import APIClient

from constants import admin_project
from constants import practice_lead_project

from ..models import Affiliate
from ..models import Affiliation
from ..models import CheckType
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
from ..models import SocMajor
from ..models import StackElement
from ..models import StackElementType
from ..models import User
from ..models import UserPermission
from .utils.load_data import load_data


# flake8 ignore=PT004
def pytest_configure(config):
    config.addinivalue_line(
        "markers", "load_user_data_required: run load_data if any tests marked"
    )


@pytest.fixture(scope="session", autouse=True)
def load_data_once_for_specific_tests(request, django_db_setup, django_db_blocker):
    # Check if any tests marked with 'load_data_required' are going to be run
    if request.node.items:
        for item in request.node.items:
            if "load_user_data_required" in item.keywords:
                with django_db_blocker.unblock():
                    print("Running load_data before any test classes in marked files")
                    load_data()
                break  # Run only once before all the test files


@pytest.fixture
def user_superuser_admin():
    return User.objects.create_user(
        username="AdminUser",
        email="adminuser@example.com",
        password="adminuser",
        is_superuser=True,
    )


@pytest.fixture
def user_permissions():
    user1 = User.objects.create(username="TestUser1", email="TestUser1@example.com")
    user2 = User.objects.create(username="TestUser2", email="TestUser2@example.com")
    project = Project.objects.create(name="Test Project")
    permission_type = PermissionType.objects.first()
    practice_area = PracticeArea.objects.first()
    user1_permission = UserPermission.objects.create(
        user=user1,
        permission_type=permission_type,
        project=project,
        practice_area=practice_area,
    )
    user2_permissions = UserPermission.objects.create(
        user=user2,
        project=project,
        permission_type=permission_type,
        practice_area=practice_area,
    )
    return [user1_permission, user2_permissions]


@pytest.fixture
def user_permission_admin_project():
    user = User.objects.create(
        username="TestUser Admin Project",
        email="TestUserAdminProject@example.com",
    )
    project = Project.objects.create(name="Test Project Admin Project")
    permission_type = PermissionType.objects.filter(name=admin_project).first()
    user_permission = UserPermission.objects.create(
        user=user,
        permission_type=permission_type,
        project=project,
    )

    return user_permission


@pytest.fixture
def user_permission_practice_lead_project():
    user = User.objects.create(
        username="TestUser Practie Lead Project",
        email="TestUserPracticeLeadProject@example.com",
    )
    permission_type = PermissionType.objects.filter(name=practice_lead_project).first()
    project = Project.objects.create(name="Test Project Admin Project")
    practice_area = PracticeArea.objects.first()
    user_permission = UserPermission.objects.create(
        user=user,
        permission_type=permission_type,
        project=project,
        practice_area=practice_area,
    )

    return user_permission


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
def event_pm(project):
    return Event.objects.create(
        name="PM",
        project=project,
        must_attend=[
            {
                "practice_area": "Development",
                "permission_type": "practiceLeadProject",
            },
            {
                "practice_area": "Design",
                "permission_type": "practiceLeadJrProject",
            },
        ],
        should_attend=[
            {
                "practice_area": "Development",
                "permission_type": "memberProject",
            },
            {"practice_area": "Design", "permission_type": "adminProject"},
        ],
        could_attend=[{"practice_area": "Design", "permission_type": "memberGeneral"}],
    )


@pytest.fixture
def event_all(project):
    return Event.objects.create(
        name="All",
        project=project,
        must_attend=[
            {
                "practice_area": "Professional Development",
                "permission_type": "adminProject",
            }
        ],
        should_attend=[],
        could_attend=[],
    )


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
def stack_element(stack_element_type):
    return StackElement.objects.create(
        name="Test Stack Element", element_type=stack_element_type
    )


@pytest.fixture
def permission_type1():
    return PermissionType.objects.create(
        name="Test Permission Type", description="", rank=1000
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
        is_sponsor=False,
        is_partner=False,
        project=project,
        affiliate=affiliate,
    )


@pytest.fixture
def check_type():
    return CheckType.objects.create(
        name="This is a test check_type.",
        description="This is a test check_type description.",
    )


@pytest.fixture
def soc_major():
    return SocMajor.objects.create(occ_code="22-2222", title="Test Soc Major")
