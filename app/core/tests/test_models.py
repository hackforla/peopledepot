import pytest


@pytest.mark.django_db
def test_user(user, django_user_model):
    assert django_user_model.objects.filter(is_staff=False).count() == 1
    assert str(user) == "testuser@email.com"
    assert user.is_django_user is True
    assert repr(user) == f"<User {user.uuid}>"


@pytest.mark.django_db
def test_project(project):
    assert str(project) == "Test Project"
