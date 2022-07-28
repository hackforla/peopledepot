from django.contrib.auth import get_user_model
from pytest import mark, raises

pytestmark = mark.django_db


def create_user(**params):
    return get_user_model().objects.create_user(**params)


def create_admin_user(**params):
    return get_user_model().objects.create_user(is_staff=True, **params)


class TestUsers:
    def setUp(self):
        # self.user = create_user(username="TestUser", password="testpass")
        self.admin_user = create_admin_user(username="TestUser2", password="testpass")

    def test_good_choice(client, django_user_model):
        create_admin_user(username="TestUser2", password="testpass")
        assert django_user_model.objects.filter(is_staff=True).count() == 1

    def test_bad_choice(client, django_user_model):
        create_admin_user(username="TestUser2", password="testpass")
        with raises(django_user_model.DoesNotExist):
            django_user_model.objects.get(username="Nobody")
