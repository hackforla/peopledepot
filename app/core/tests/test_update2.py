# test_update.py
from .base import BaseTestCase
import pytest

@pytest.mark.django_db
class TestUpdate(BaseTestCase):
    # wally_user - see setUpTestData

    def test_wally_user_exists(self):
        wally_user = self.wally_user
        assert(wally_user is not None)
