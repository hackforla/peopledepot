import pytest
from django.urls import reverse
from rest_framework import status

from core.api.serializers import UserSerializer

ME_URL = reverse("my_profile")
USERS_URL = reverse("user-list")
CREATE_USER_PAYLOAD = {
    "username": "TestUserAPI",
    "password": "testpass",
    # time_zone is required because django_timezone_field doesn't yet support the blank string
    "time_zone": "America/Los_Angeles",
}


def create_user(django_user_model, **params):
    return django_user_model.objects.create_user(**params)


@pytest.mark.django_db
def test_list_users_fail(client):
    res = client.get(USERS_URL)

    assert res.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_get_profile(auth_client):
    res = auth_client.get(ME_URL)

    assert res.status_code == status.HTTP_200_OK
    assert res.data["username"] == "TestUser"


@pytest.mark.django_db
def test_get_users(auth_client, django_user_model):
    create_user(django_user_model, username="TestUser2", password="testpass")
    create_user(django_user_model, username="TestUser3", password="testpass")

    res = auth_client.get(USERS_URL)

    assert res.status_code == status.HTTP_200_OK
    assert len(res.data) == 3

    users = django_user_model.objects.all().order_by("created_at")
    serializer = UserSerializer(users, many=True)
    assert res.data == serializer.data


@pytest.mark.django_db
def test_get_single_user(auth_client, user):
    res = auth_client.get(f"{USERS_URL}?email={user.email}")
    assert res.status_code == status.HTTP_200_OK

    res = auth_client.get(f"{USERS_URL}?username={user.username}")
    assert res.status_code == status.HTTP_200_OK


users_actions_test_data = [
    (
        "admin_client",
        "post",
        USERS_URL,
        CREATE_USER_PAYLOAD,
        status.HTTP_201_CREATED,
    ),
    ("admin_client", "get", USERS_URL, {}, status.HTTP_200_OK),
    (
        "auth_client",
        "post",
        USERS_URL,
        {"username": "TestUser2", "password": "testpass"},
        status.HTTP_403_FORBIDDEN,
    ),
    ("auth_client", "get", USERS_URL, {}, status.HTTP_200_OK),
]


@pytest.mark.django_db
@pytest.mark.parametrize(
    "client_name,action,endpoint,payload,expected_status",
    users_actions_test_data,
)
def test_users_actions(
    client_name, action, endpoint, payload, expected_status, request
):

    client = request.getfixturevalue(client_name)
    action_fn = getattr(client, action)
    res = action_fn(endpoint, payload)
    assert res.status_code == expected_status


user_actions_test_data = [
    ("auth_client", "patch", {"first_name": "TestUser2"}, status.HTTP_200_OK),
    (
        "auth_client",
        "put",
        CREATE_USER_PAYLOAD,
        status.HTTP_200_OK,
    ),
    ("auth_client", "delete", {}, status.HTTP_403_FORBIDDEN),
    ("admin_client", "patch", {"first_name": "TestUser2"}, status.HTTP_403_FORBIDDEN),
    (
        "admin_client",
        "put",
        CREATE_USER_PAYLOAD,
        status.HTTP_403_FORBIDDEN,
    ),
    ("admin_client", "delete", {}, status.HTTP_204_NO_CONTENT),
    ("auth_client2", "patch", {"first_name": "TestUser2"}, status.HTTP_403_FORBIDDEN),
    (
        "auth_client2",
        "put",
        CREATE_USER_PAYLOAD,
        status.HTTP_403_FORBIDDEN,
    ),
    ("auth_client2", "delete", {}, status.HTTP_403_FORBIDDEN),
]


@pytest.mark.django_db
@pytest.mark.parametrize(
    "client_name,action,payload,expected_status", user_actions_test_data
)
def test_user_actions(client_name, user, action, payload, expected_status, request):

    endpoint = reverse("user-detail", kwargs={"pk": user.uuid})
    client = request.getfixturevalue(client_name)
    action_fn = getattr(client, action)
    res = action_fn(endpoint, payload)
    assert res.status_code == expected_status
