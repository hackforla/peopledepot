import pytest

from core.models import User
from core.models import UserPermissions


class TestSetup:
    @pytest.mark.django_db
    def test_wanda_setup(self):
        user = User.objects.get(username="Wanda")
        assert user is not None
        permission_count = UserPermissions.objects.count()
        assert permission_count > 0
