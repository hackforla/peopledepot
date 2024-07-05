import pytest

from core.models import User


class TestSetup:
    @pytest.mark.django_db
    def test_setup(self):
        user = User.objects.get(username="Garry")
        assert user is not None

    @pytest.mark.django_db
    def test_setup2(self):
        user = User.objects.get(username="Valerie")
        assert user is not None
