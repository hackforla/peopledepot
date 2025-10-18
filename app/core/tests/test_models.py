import re

import pytest
from django.db import IntegrityError
from django.db.models.deletion import ProtectedError

from ..models import Event
from ..models import PracticeArea
from ..models import ProgramArea
from ..models import ProjectProgramAreaXref
from ..models import ProjectSdgXref
from ..models import ProjectStackElementXref
from ..models import ProjectStatus
from ..models import ProjectUrl
from ..models import ReferrerType
from ..models import Sdg
from ..models import User
from ..models import UserStatusType

pytestmark = pytest.mark.django_db


def test_user(user, django_user_model):
    assert django_user_model.objects.filter(is_staff=False).count() == 1
    assert str(user) == "testuser@email.com"
    assert user.is_django_user is True
    assert repr(user) == f"<User {user.uuid}>"


def test_project(project):
    assert str(project) == "Test Project"


def filter_objects_by_name(objects_list, name):
    return [obj for obj in objects_list if getattr(obj, "name", None) == name]


def test_event_projects_admins_must_attend(event_all, event_pm):
    projects_admins_must_attend = Event.objects.filter(
        must_attend__contains=[{"permission_type": "adminProject"}]
    )

    assert projects_admins_must_attend.count() == 1
    assert len(filter_objects_by_name(projects_admins_must_attend, "All")) == 1
    assert len(filter_objects_by_name(projects_admins_must_attend, "PM")) == 0


def test_practice_area(practice_area):
    assert str(practice_area) == "Test Practice Area"


def test_affiliate(affiliate):
    assert str(affiliate) == "Test Affiliate"


def test_faq(faq):
    assert str(faq) == "Test Faq"


def test_faq_viewed(faq_viewed):
    assert str(faq_viewed).startswith("Test Faq viewed")


def test_location(location):
    assert str(location) == "Test Hack for L.A. HQ"


def test_program_area(program_area):
    assert str(program_area) == "Test Program Area"


def test_skill(skill):
    assert str(skill) == "Test Skill"


def test_stack_element(stack_element):
    assert str(stack_element) == "Test Stack Element"


def test_permission_type1(permission_type1):
    assert str(permission_type1.name) == "Test Permission Type"
    assert str(permission_type1.description) == ""
    assert str(permission_type1) == "Test Permission Type"


def test_permission_type2(permission_type2):
    assert str(permission_type2.name) == "Test Permission Type"
    assert str(permission_type2.description) == "A permission type description"
    assert (
        str(permission_type2) == "Test Permission Type: A permission type description"
    )


def test_stack_element_type(stack_element_type):
    assert str(stack_element_type) == "Test Stack Element Type"


def test_sdg(sdg):
    assert str(sdg) == "Test SDG name"


def test_affiliation_sponsor(affiliation1):
    xref_instance = affiliation1
    assert xref_instance.is_sponsor is True
    assert xref_instance.is_partner is False
    assert str(xref_instance) == f"Sponsor {xref_instance.project}"


def test_user_permission_admin_project(user_permission_admin_project):
    user_permission = user_permission_admin_project
    username = user_permission.user.username
    permission_type_name = user_permission.permission_type.name
    project_name = user_permission.project.name
    pattern = f".*{username}.*{permission_type_name}.*{project_name}"
    assert re.search(pattern, str(user_permission))


def test_user_permission_practice_lead_project(user_permission_practice_lead_project):
    user_permission = user_permission_practice_lead_project
    username = user_permission.user.username
    permission_type_name = user_permission.permission_type.name
    project_name = user_permission.project.name
    practice_area_name = user_permission.practice_area.name
    pattern = (
        f".*{username}.*{permission_type_name}.*{project_name}.*{practice_area_name}"
    )
    assert re.search(pattern, str(user_permission))


def test_affiliation_partner(affiliation2):
    xref_instance = affiliation2
    assert xref_instance.is_sponsor is False
    assert xref_instance.is_partner is True
    assert str(xref_instance) == f"Partner {xref_instance.affiliate}"


def test_affiliation_partner_and_sponsor(affiliation3):
    xref_instance = affiliation3
    assert xref_instance.is_sponsor is True
    assert xref_instance.is_partner is True
    assert (
        str(xref_instance)
        == f"Sponsor {xref_instance.project} and Partner {xref_instance.affiliate}"
    )


def test_affiliation_is_neither_partner_and_sponsor(affiliation4):
    xref_instance = affiliation4
    assert xref_instance.is_sponsor is False
    assert xref_instance.is_partner is False
    assert str(xref_instance) == "Neither a partner or a sponsor"


def test_check_type(check_type):
    assert str(check_type) == "This is a test check_type."
    assert check_type.description == "This is a test check_type description."


def test_event_type(event_type):
    assert str(event_type) == "This is a test event_type."
    assert event_type.description == "This is a test event_type description."


def test_leadership_type(leadership_type):
    assert str(leadership_type) == "This is a test leadership_type"
    assert leadership_type.description == "This is a test leadership_type description"


def test_leadership_type_project_relationship(project, leadership_type):
    assert project.leadership_type is None
    project.leadership_type = leadership_type
    assert project.leadership_type == leadership_type


def test_soc_major(soc_major):
    assert str(soc_major) == "Test Soc Major"


def test_soc_minor(soc_minor):
    assert str(soc_minor) == "Test Soc Minor"


def test_soc_major_soc_minor_relationship(soc_major, soc_minor):
    assert soc_minor.soc_major is None
    soc_minor.soc_major = soc_major
    assert soc_minor.soc_major == soc_major


def test_project_program_area_relationship(project):
    workforce_development_program_area = ProgramArea.objects.get(
        name="Workforce Development"
    )
    project.program_areas.add(workforce_development_program_area)
    assert project.program_areas.count() == 1
    assert project.program_areas.contains(workforce_development_program_area)
    assert workforce_development_program_area.projects.contains(project)
    workforce_development_program_area_xref = ProjectProgramAreaXref.objects.get(
        project=project, program_area=workforce_development_program_area
    )
    assert workforce_development_program_area_xref.created_at is not None
    project.program_areas.remove(workforce_development_program_area)
    assert project.program_areas.count() == 0
    assert not workforce_development_program_area.projects.contains(project)
    assert not project.program_areas.contains(workforce_development_program_area)


def test_project_sdg_relationship(project):
    climate_action_sdg = Sdg.objects.get(name="Climate Action")

    project.sdgs.add(climate_action_sdg)
    assert project.sdgs.count() == 1
    assert project.sdgs.contains(climate_action_sdg)
    assert climate_action_sdg.projects.contains(project)

    climate_action_sdg_xref = ProjectSdgXref.objects.get(
        project_id=project,
        sdg_id=climate_action_sdg,
    )
    assert climate_action_sdg_xref.ended_on is None

    project.sdgs.remove(climate_action_sdg)
    assert project.sdgs.count() == 0
    assert not project.sdgs.contains(climate_action_sdg)
    assert not climate_action_sdg.projects.contains(project)


def test_project_status(project_status):
    assert str(project_status) == "This is a test project_status"
    assert project_status.description == "This is a test project_status"


def test_project_has_a_project_status_relationship(
    project_1,
    project_2,
):
    active_project_status = ProjectStatus.objects.get(name="Active")
    closed_project_status = ProjectStatus.objects.get(name="Closed")

    active_project_status.project_set.add(project_1)
    active_project_status.project_set.add(project_2)
    assert active_project_status.project_set.count() == 2

    assert project_1.current_status == active_project_status
    assert project_2.current_status == active_project_status

    active_project_status.project_set.remove(project_1)
    closed_project_status.project_set.add(project_1)

    assert active_project_status.project_set.count() == 1
    assert closed_project_status.project_set.count() == 1

    assert project_1.current_status == closed_project_status


def test_url_type(url_type):
    assert str(url_type) == "This is a test url type name"


def test_user_status_type(user_status_type):
    assert str(user_status_type) == "Test User Status Type"


def test_referrer_type(referrer_type):
    assert str(referrer_type) == "Test Referrer Type"


def test_referrer(referrer):
    assert str(referrer) == "This is a test referrer"


def test_referrer_has_a_referrer_type(referrer):
    bootcamp_referrer_type = ReferrerType.objects.get(name="Bootcamp")
    bootcamp_referrer_type.referrer_set.add(referrer)
    assert bootcamp_referrer_type.referrer_set.count() == 1

    assert referrer.referrer_type == bootcamp_referrer_type
    bootcamp_referrer_type.referrer_set.remove(referrer)
    assert bootcamp_referrer_type.referrer_set.count() == 0


def test_user_model_old_names():
    """
    Test that accessing old field names raises AttributeError.
    """
    old_fields = [
        "current_job_title",
        "gmail",
        "preferred_email",
        "target_job_title",
    ]
    for field in old_fields:
        if not hasattr(User, field):
            with pytest.raises(
                AttributeError, match=f"type object 'User' has no attribute '{field}'"
            ):
                getattr(User, field)


def test_user_has_a_user_status_relationship(user, user2):
    active_user_status = UserStatusType.objects.get(name="Active")
    inactive_user_status = UserStatusType.objects.get(name="Inactive")
    active_user_status.user_set.add(user)
    active_user_status.user_set.add(user2)

    assert active_user_status.user_set.count() == 2

    assert user.user_status == active_user_status
    assert user2.user_status == active_user_status

    inactive_user_status.user_set.add(user)

    assert active_user_status.user_set.count() == 1
    assert inactive_user_status.user_set.count() == 1

    assert user.user_status == inactive_user_status


def test_user_practice_area_relationship(user, user2):
    development_practice_area = PracticeArea.objects.get(name="Development")
    project_management_practice_area = PracticeArea.objects.get(
        name="Project Management"
    )
    # design_practice_area = PracticeArea.objects.get(name="Design")

    user.practice_area_primary = development_practice_area
    user.save()
    assert user.practice_area_primary == development_practice_area
    assert development_practice_area.primary_users.filter(uuid=user.uuid).exists()

    user.practice_area_primary = None
    user.save()
    assert user.practice_area_primary is None
    assert not development_practice_area.primary_users.filter(uuid=user.uuid).exists()

    user2.practice_area_secondary.add(project_management_practice_area)
    assert user2.practice_area_secondary.count() == 1
    assert user2.practice_area_secondary.contains(project_management_practice_area)
    assert project_management_practice_area.secondary_users.contains(user2)

    user2.practice_area_secondary.remove(project_management_practice_area)
    assert user2.practice_area_secondary.count() == 0
    assert not user2.practice_area_secondary.contains(project_management_practice_area)
    assert not project_management_practice_area.secondary_users.contains(user2)


def test_project_url(project_url):
    assert project_url is not None

    assert project_url.project is not None
    assert project_url.url_type is not None

    assert project_url.name == "This is a test project url"
    assert project_url.external_id == "This is a test external id"

    assert project_url.url == "https://test.com"

    assert str(project_url) == "This is a test project url"


def test_project_stack_element_relationship(project, stack_element):
    """
    Verify that a Project can be linked to a StackElement via ProjectStackElementXref.
    """
    # Create the cross-reference record
    xref = ProjectStackElementXref.objects.create(
        project=project, stack_element=stack_element
    )

    # Check string representation
    assert str(xref) == f"Project: {project.name} -> StackElement: {stack_element.name}"

    # Forward relationships
    assert xref.project == project
    assert xref.stack_element == stack_element
    assert xref.created_at is not None  # from AbstractBaseModel

    # Reverse relationships
    assert project.stack_elements.filter(pk=stack_element.pk).exists()
    assert stack_element.projects.filter(pk=project.pk).exists()


def test_project_stack_element_unique_constraint(project, stack_element):
    """
    Ensure that duplicate project-stack_element pairs are prevented
    by the unique constraint on ProjectStackElementXref.
    """
    # First insert is fine
    ProjectStackElementXref.objects.create(project=project, stack_element=stack_element)

    # Second insert with same project + stack_element should fail
    with pytest.raises(IntegrityError):
        ProjectStackElementXref.objects.create(
            project=project, stack_element=stack_element
        )


def test_url_status_type_str(url_status_type):
    # __str__ returns the name
    assert str(url_status_type) == "active"


def test_project_url_can_set_status(project_url, url_status_type):
    # Set FK and save
    project_url.url_status_type = url_status_type
    project_url.save()

    # Reload & assert
    pu = ProjectUrl.objects.get(pk=project_url.pk)
    assert pu.url_status_type == url_status_type


def test_url_status_type_reverse_relation(project_url, url_status_type):
    # Attach and verify reverse relation works
    project_url.url_status_type = url_status_type
    project_url.save()

    # Default reverse accessor: <ModelName>_set
    assert url_status_type.projecturl_set.count() == 1
    assert url_status_type.projecturl_set.first().pk == project_url.pk


def test_protect_deletion_when_in_use(project_url, url_status_type):
    # PROTECT should block deletion while referenced
    project_url.url_status_type = url_status_type
    project_url.save()

    with pytest.raises(ProtectedError):
        url_status_type.delete()


def test_status_is_nullable(project_url):
    # Field allows null=True; default should be None unless set
    assert project_url.url_status_type is None
