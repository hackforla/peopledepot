from django.contrib.auth import get_user_model
import pytest


@pytest.mark.django_db
def test_user(user):
    assert get_user_model().objects.filter(is_staff=False).count() == 1
    assert str(user) == "testuser@email.com"
    assert user.is_django_user == True
    assert repr(user) == f"<User {user.uuid}>"
