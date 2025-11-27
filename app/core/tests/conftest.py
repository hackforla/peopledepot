import pytest
from rest_framework.test import APIClient

from constants import admin_project
from constants import practice_lead_project

from ..models import Affiliate
from ..models import Affiliation
from ..models import CheckType
from ..models import Event
from ..models import EventType
from ..models import Faq
from ..models import FaqViewed
from ..models import LeadershipType
from ..models import Location
from ..models import Organization
from ..models import PermissionType
from ..models import PracticeArea
from ..models import ProgramArea
from ..models import Project
from ..models import ProjectStackElementXref
from ..models import ProjectStatus
from ..models import ProjectUrl
from ..models import Referrer
from ..models import ReferrerType
from ..models import Sdg
from ..models import Skill
from ..models import SocBroad
from ..models import SocMajor
from ..models import SocMinor
from ..models import StackElement
from ..models import StackElementType
from ..models import UrlStatusType
from ..models import UrlType
from ..models import User
from ..models import UserCheck
from ..models import UserPermission
from ..models import UserStatusType
from ..models import Win
from ..models import WinType


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
        username="TestUser Admin Project", email="TestUserAdminProject@example.com"
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
            {"practice_area": "Development", "permission_type": "practiceLeadProject"},
            {"practice_area": "Design", "permission_type": "practiceLeadJrProject"},
        ],
        should_attend=[
            {"practice_area": "Development", "permission_type": "memberProject"},
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
def leadership_type():
    return LeadershipType.objects.create(
        name="This is a test leadership_type",
        description="This is a test leadership_type description",
    )


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
def sdg1():
    return Sdg.objects.create(name="Test SDG name1")


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


@pytest.fixture
def check_type():
    return CheckType.objects.create(
        name="This is a test check_type.",
        description="This is a test check_type description.",
    )


@pytest.fixture
def event_type():
    return EventType.objects.create(
        name="This is a test event_type.",
        description="This is a test event_type description.",
    )


@pytest.fixture
def project_1():
    return Project.objects.create(name="Project 1")


@pytest.fixture
def project_2():
    return Project.objects.create(name="Project 2")


@pytest.fixture
def project_status():
    return ProjectStatus.objects.create(
        name="This is a test project_status",
        description="This is a test project_status",
    )


@pytest.fixture
def soc_broad(soc_minor):
    return SocBroad.objects.create(
        soc_minor=soc_minor,
        occ_code="15-1252",
        title="Software Developers",
    )


@pytest.fixture
def soc_major():
    return SocMajor.objects.create(occ_code="22-2222", title="Test Soc Major")


@pytest.fixture
def soc_minor():
    return SocMinor.objects.create(occ_code="22-2222", title="Test Soc Minor")


@pytest.fixture
def url_type():
    return UrlType.objects.create(
        name="This is a test url type name",
        description="This is a test url type description",
    )


@pytest.fixture
def user_status_type():
    return UserStatusType.objects.create(
        name="Test User Status Type", description="Test User Status Type description"
    )


@pytest.fixture
def referrer_type():
    return ReferrerType.objects.create(
        name="Test Referrer Type", description="Test Referrer Type description"
    )


@pytest.fixture
def referrer(referrer_type):
    return Referrer.objects.create(
        name="This is a test referrer",
        referrer_type=referrer_type,
        contact_name="John Doe",
        contact_email="john@example.com",
    )


@pytest.fixture
def project_url(project, url_type):
    return ProjectUrl.objects.create(
        project=project,
        url_type=url_type,
        name="This is a test project url",
        external_id="This is a test external id",
        url="https://test.com",
    )


@pytest.fixture
def project_stack_element_xref(project, stack_element):
    """
    Fixture to create and return a ProjectStackElementXref record
    linking a project and a stack element.
    """
    return ProjectStackElementXref.objects.create(
        project=project, stack_element=stack_element
    )


@pytest.fixture
def url_status_type(db):
    return UrlStatusType.objects.create(
        name="active", description="URL is live and valid"
    )


@pytest.fixture
def organization():
    return Organization.objects.create(
        name="Hack for LA",
        time_zone="America/Los_Angeles",
    )


@pytest.fixture
def user_check(user, organization, check_type, project):
    return UserCheck.objects.create(
        user=user,
        org=organization,
        check_type=check_type,
        result=None,
        reminder_start=None,
        completed_at=None,
        project=project,
    )


@pytest.fixture
def win(user, practice_area, project, win_type):
    win_obj = Win.objects.create(
        user=user,
        description="Got funding for the project",
        win_type=win_type,
        can_use_photo=True,
    )
    win_obj.practice_areas.add(practice_area)
    win_obj.teams.add(project)
    return win_obj


@pytest.fixture
def win_type():
    return WinType.objects.create(
        name="funding",
        display_text="Funding / Grant awarded",
    )
