import pytest

from core.models import User
from core.models import UserPermission


class TestSetup:
    @pytest.mark.skip
    @pytest.mark.django_db
    def test_wanda_setup(self):
        user = User.objects.get(username="Wanda")
        assert user is not None
        permission_count = UserPermission.objects.count()
        assert permission_count > 0
