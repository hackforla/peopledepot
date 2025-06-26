import re

import pytest

from ..models import Event
from ..models import ProgramArea
from ..models import ProjectProgramAreaXref
from ..models import ProjectSdgXref
from ..models import ProjectStatus
from ..models import ReferrerType
from ..models import Sdg

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
