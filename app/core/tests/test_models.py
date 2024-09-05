import pytest
from django.test import TestCase

from ..models import Event
from ..models import ProgramArea
from ..models import Project
from ..models import ProjectProgramAreaXref

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


def test_technology(technology):
    assert str(technology) == "Test Technology"


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


class ProjectProgramAreaXrefTestCase(TestCase):
    def setUp(self):
        # retrieve the objects from the DB
        self.program_area1 = ProgramArea.objects.get(name="Workforce Development")
        self.program_area2 = ProgramArea.objects.get(name="Civic Tech Infrastructure")

        # Create a Project object
        self.project = Project.objects.create(name="Hack for LA Site")

        # Create ProjectProgramAreaXref objects to link the project to program areas
        self.project_program_area_xref1 = ProjectProgramAreaXref.objects.create(
            project_id=self.project,
            program_area_id=self.program_area1,
            created_date="2024-08-30 02:34:00",
        )
        self.project_program_area_xref2 = ProjectProgramAreaXref.objects.create(
            project_id=self.project,
            program_area_id=self.program_area2,
            created_date="2024-08-30 02:34:00",
        )

    def test_project_to_program_areas_relationship(self):
        # Get all ProgramAreas associated with the project
        program_areas = ProgramArea.objects.filter(
            projectprogramareaxref__project_id=self.project
        )
        assert program_areas.count() == 2
        # check if program_area1 is included in the retrieved program_areas
        assert self.program_area1 in program_areas
        assert self.program_area2 in program_areas

    def test_program_area_to_projects_relationship(self):
        # Get all Projects associated with the first ProgramArea
        projects_for_area1 = Project.objects.filter(
            projectprogramareaxref__program_area_id=self.program_area1
        )
        assert projects_for_area1.count() == 1
        # asserts that self.project is included in the retrieved projects_for_area1
        assert self.project in projects_for_area1

        # Get all Projects associated with the second ProgramArea
        projects_for_area2 = Project.objects.filter(
            projectprogramareaxref__program_area_id=self.program_area2
        )
        assert projects_for_area2.count() == 1
        assert self.project in projects_for_area2
