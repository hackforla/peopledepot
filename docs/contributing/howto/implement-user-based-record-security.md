# Record-Level Security for User-Related Tables

This guide explains how to **add record-level security** to a table related to users, such as `UserPermission`.

---

## 1. General Principle

- Record-level security ensures that **a user can only view or modify records they are authorized to access**.
- For tables like `UserPermission`, this usually means:
    - Users can see their own permissions.
    - Admins can see all permissions.
    - Project-level admins can see permissions for users in projects they manage.

---

## 2. Queryset Filtering

- **All record-level filtering is handled in `UserRelatedRequest.get_queryset()`**.
- Example usage in a viewset:

```python
from core.models import UserPermission
from core.access_control import UserRelatedRequest


class UserPermissionViewSet(ModelViewSet):
    serializer_class = UserPermissionSerializer

    def get_queryset(self):
        # Returns a queryset already filtered for the requesting user
        return UserRelatedRequest.get_queryset(view=self)
```

- **Notes**:
    - `get_queryset()` internally calls `get_permitted_users()` and applies any project or admin-based filtering.
    - This ensures **GET/list operations only return records the user is allowed to see**.

---

## 3. Field-Level and Record-Level Enforcement on Mutations

- Use `UserRelatedRequest.validate_post_fields()` and `validate_patch_fields()` to enforce **field-level security** when creating or updating records:

```python
from rest_framework.permissions import BasePermission
from core.access_control import UserRelatedRequest


class HasUserPermissionRecord(BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST":
            UserRelatedRequest.validate_post_fields(view, request)
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in ["PATCH", "DELETE"]:
            UserRelatedRequest.validate_patch_fields(view, request, obj)
        return True
```

- Apply this permission class to the viewset:

```python
class UserPermissionViewSet(ModelViewSet):
    serializer_class = UserPermissionSerializer
    permission_classes = [HasUserPermissionRecord]

    def get_queryset(self):
        # Record-level filtering is handled here
        return UserRelatedRequest.get_queryset(view=self)
```

---

## 4. Best Practices

1. **Always use `UserRelatedRequest.get_queryset()`** to enforce record-level security.
1. **Always validate POST/PATCH fields** to prevent unauthorized modifications.
1. **Admin users** can bypass normal restrictions via `AccessControl.is_admin()`.
1. **Document your rules**: which roles can access which records under what conditions.
1. **Test thoroughly**:
    - Normal users cannot see or modify other users’ records.
    - Project admins can modify records for their projects only.
    - Global admins can access all records.

---

## 5. Summary

For user-related tables like `UserPermission`:

- **Record-level filtering is centralized in `UserRelatedRequest.get_queryset()`**.
- **Field-level validation** ensures safe creation and updates.
- Together, this provides a secure, maintainable, and consistent record-level access control system.
