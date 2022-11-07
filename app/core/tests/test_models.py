import pytest

pytestmark = pytest.mark.django_db


def test_user(user, django_user_model):
    assert django_user_model.objects.filter(is_staff=False).count() == 1
    assert str(user) == "testuser@email.com"
    assert user.is_django_user is True
    assert repr(user) == f"<User {user.uuid}>"


def test_project(project):
    assert str(project) == "Test Project"


def test_recurring_event(recurring_event):
    assert str(recurring_event) == "Test Recurring Event"


def test_faq(faq):
    assert str(faq) == "Test Faq"


# def test_faq_viewed(faq, faq_viewed):
#     assert str(f"{faq} viewed") == "Test Faq viewed"
#     assert str(f"{faq_viewed.faq.question}") == f"{faq.question}"
#     assert repr(faq_viewed) == f"<Faq_viewed {faq_viewed.uuid}>"
#     assert repr(faq_viewed.faq) == f"<Faq {faq.uuid}>"
def test_faq_viewed(faq_viewed):
    assert str(f"{faq_viewed.faq}") == "Test Faq"
    # assert str(f"{faq_viewed.read}") == "Test Faq_viewed read"
