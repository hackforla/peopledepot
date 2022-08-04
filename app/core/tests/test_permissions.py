import pytest
from core.api.permissions import DenyAny, IsOwnerOrReadOnly
from django.test import RequestFactory

pytestmark = pytest.mark.django_db

no_permission_test_data = [
    ("get", False),
    ("post", False),
    ("put", False),
    ("patch", False),
    ("delete", False),
]

@pytest.mark.parametrize("action,expected_permission", no_permission_test_data)
def test_denyany_owner_permission(user, rf, action, expected_permission):
    """
    Owner has no permission under DenyAny
    """
    action_fn = getattr(rf, action)
    request = action_fn("/")
    request.user = user

    assert DenyAny().has_permission(request, None) == expected_permission
    assert DenyAny().has_object_permission(request, None, user) == expected_permission

@pytest.mark.parametrize("action,expected_permission", no_permission_test_data)
def test_denyany_notowner_permission(user, user2, rf, action, expected_permission):
    """
    Other has no permission under DenyAny
    """
    action_fn = getattr(rf, action)
    request = action_fn("/")
    request.user = user2

    assert DenyAny().has_permission(request, None) == expected_permission
    assert DenyAny().has_object_permission(request, None, user) == expected_permission

@pytest.mark.parametrize("action,expected_permission", no_permission_test_data)
def test_denyany_admin_permission(admin, user, rf, action, expected_permission):
    """
    Admin has no permission under DenyAny
    """
    action_fn = getattr(rf, action)
    request = action_fn("/")
    request.user = admin

    assert DenyAny().has_permission(request, None) == expected_permission
    assert DenyAny().has_object_permission(request, None, user) == expected_permission

full_permission_test_data = [
    ("get", True),
    ("post", True),
    ("put", True),
    ("patch", True),
    ("delete", True),
]

@pytest.mark.parametrize("action,expected_permission", full_permission_test_data)
def test_isownerorreadonly_user_permission(user, rf, action, expected_permission):
    """
    Owner has full permission under IsOwnerOrReadOnly
    """
    action_fn = getattr(rf, action)
    request = action_fn("/")
    request.user = user

    assert IsOwnerOrReadOnly().has_object_permission(request, None, user) == expected_permission

readonly_permission_test_data = [
    ("get", True),
    ("post", False),
    ("put", False),
    ("patch", False),
    ("delete", False),
]

@pytest.mark.parametrize("action,expected_permission", readonly_permission_test_data)
def test_isownerorreadonly_notowner_permission(user, user2, rf, action, expected_permission):
    """
    Other user has read permission under IsOwnerOrReadOnly
    """
    action_fn = getattr(rf, action)
    request = action_fn("/")
    request.user = user2

    assert IsOwnerOrReadOnly().has_object_permission(request, None, user) == expected_permission


@pytest.mark.parametrize("action,expected_permission", readonly_permission_test_data)
def test_isownerorreadonly_admin_permission(admin, user, rf, action, expected_permission):
    """
    Admin has read permission under IsOwnerOrReadOnly
    """
    action_fn = getattr(rf, action)
    request = action_fn("/")
    request.user = admin

    assert IsOwnerOrReadOnly().has_object_permission(request, None, user) == expected_permission

def test_notowner_cannot_delete(user, user2, rf):
    """
    Extra single that other user is denied delete permission
    """
    request = rf.delete("/")
    request.user = user2

    assert IsOwnerOrReadOnly().has_object_permission(request, None, user) == False
