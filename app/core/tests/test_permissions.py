import pytest

from core.api.permissions import DenyAny

pytestmark = pytest.mark.django_db

no_permission_test_data = [
    ("get", False),
    ("post", False),
    ("put", False),
    ("patch", False),
    ("delete", False),
]


@pytest.mark.parametrize(("action", "expected_permission"), no_permission_test_data)
def test_denyany_owner_permission(user, rf, action, expected_permission):
    """
    Owner has no permission under DenyAny
    """
    action_fn = getattr(rf, action)
    request = action_fn("/")
    request.user = user

    assert DenyAny().has_permission(request, None) == expected_permission
    assert DenyAny().has_object_permission(request, None, user) == expected_permission


@pytest.mark.parametrize(("action", "expected_permission"), no_permission_test_data)
def test_denyany_notowner_permission(user, user2, rf, action, expected_permission):
    """
    Other has no permission under DenyAny
    """
    action_fn = getattr(rf, action)
    request = action_fn("/")
    request.user = user2

    assert DenyAny().has_permission(request, None) == expected_permission
    assert DenyAny().has_object_permission(request, None, user) == expected_permission


@pytest.mark.parametrize(("action", "expected_permission"), no_permission_test_data)
def test_denyany_admin_permission(admin, user, rf, action, expected_permission):
    """
    Admin has no permission under DenyAny
    """
    action_fn = getattr(rf, action)
    request = action_fn("/")
    request.user = admin

    assert DenyAny().has_permission(request, None) == expected_permission
    assert DenyAny().has_object_permission(request, None, user) == expected_permission
