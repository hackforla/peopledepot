from django.test.runner import DiscoverRunner

from core.models import User


class CustomTestRunner(DiscoverRunner):
    def setup_test_environment(self, **kwargs):
        super().setup_test_environment(**kwargs)
        # Custom setup logic
        self.populate_database()

    def populate_database(self):
        print("Setting up database with initial data...")
        User.objects.create_user("testuser", password="testpassword")
        User.objects.create_user("anotheruser", password="anotherpassword")
        assert User.objects.get(username="testuser") is not None

    def teardown_test_environment(self, **kwargs):
        super().teardown_test_environment(**kwargs)
        # Custom teardown logic if needed
        print("Tearing down test environment...")
