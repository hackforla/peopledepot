import pytest
from rest_framework.test import APIClient

<<<<<<< HEAD
from ..models import Faq, Faq_viewed, Project, RecurringEvent
=======
from ..models import Project, RecurringEvent, SponsorPartner, Faq
>>>>>>> 3d609d1 (created tests)


@pytest.fixture
def user(django_user_model):
    return django_user_model.objects.create_user(
        username="TestUser",
        email="testuser@email.com",
        password="testpass",
    )


@pytest.fixture
def user2(django_user_model):
    return django_user_model.objects.create_user(
        username="TestUser2",
        email="testuser2@email.com",
        password="testpass",
    )


@pytest.fixture
def admin(django_user_model):
    return django_user_model.objects.create_user(
        is_staff=True,
        username="TestAdminUser",
        email="testadmin@email.com",
        password="testadmin",
    )


@pytest.fixture
def project():
    return Project.objects.create(name="Test Project")


@pytest.fixture
def recurring_event(project):
    return RecurringEvent.objects.create(name="Test Recurring Event", project=project)


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def auth_client(user, client):
    client.force_authenticate(user=user)
    return client


@pytest.fixture
def auth_client2(user2, client):
    client.force_authenticate(user=user2)
    return client


@pytest.fixture
def admin_client(admin, client):
    client.force_authenticate(user=admin)
    return client


@pytest.fixture
def sponsor_partner():
    return SponsorPartner.objects.create(partner_name="Test Sponsor Partner")


@pytest.fixture
def faq():
    return Faq.objects.create(question="Test Faq")
