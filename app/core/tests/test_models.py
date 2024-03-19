import pytest

pytestmark = pytest.mark.django_db


def test_user(user, django_user_model):
    assert django_user_model.objects.filter(is_staff=False).count() == 1
    assert str(user) == "testuser@email.com"
    assert user.is_django_user is True
    assert repr(user) == f"<User {user.uuid}>"


def test_project(project):
    assert str(project) == "Test Project"


def test_event(event):
    assert str(event) == "Test Event"


def test_practice_area(practice_area):
    assert str(practice_area) == "Test Practice Area"


def test_sponsor_partner(sponsor_partner):
    assert str(sponsor_partner) == "Test Sponsor Partner"


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
