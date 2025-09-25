# Access Control System Documentation

This document explains the flow of **field-level and user-level access control** in the system. It covers the roles of:

- `AccessControl` (permission rules and field filtering)  
- `UserRelatedRequest` (queryset and request validation logic for user)  
- `HasUserPermission` (DRF permission class enforcement for user)  

---

## 1. Components

### `AccessControl`
- Provides static methods to check and enforce **permissions**.  
- Responsibilities:
  - `is_admin(user)` → Check if user has the `ADMIN_GLOBAL` permission.  
  - `get_rank_dict()` → Returns permission ranks (higher rank = higher privilege).  
  - `get_csv_field_permissions()` → Reads CSV to load field-level permissions.  
  - `get_permitted_fields()` → Determines allowed fields for `get`, `post`, or `patch`.  
  - `get_most_privileged_perm_type()` → Finds the strongest permission type between two users.  
  - `has_field_permission()` → Evaluates if a given permission type allows access to a specific field.  
  *(Used primarily in `UserRelatedRequest` and `HasUserPermission` logic, called from **serializers.py** and **views.py**.)*

---

### `UserRelatedRequest`
- Provides logic for **filtering querysets** and **validating request data**.  
- Responsibilities:
  - `get_allowed_users(request)` → Returns the set of users the requester is allowed to view. (**views.py**)  
  - `get_queryset(view)` → Restricts view queryset based on allowed users. (**views.py**)  
  - `get_serializer_representation(...)` → Filters serialized output fields dynamically based on permissions. (**serializers.py**)  
  - `validate_post_fields(view, request)` → Ensures only permitted fields are used in a POST request. (**views.py**)  
  - `validate_patch_fields(view, request, obj)` → Ensures only permitted fields are used in a PATCH request. (**views.py**)  
  - `validate_request_fields(request, valid_fields)` → Core enforcement: raises `PermissionDenied` or `ValidationError` if unauthorized fields are used.  

---

### `HasUserPermission`
- A **Django REST Framework permission class**.  
- Enforces rules at both the **request** and **object** level.  
- Responsibilities:
  - `has_permission()` → On POST, calls `UserRelatedRequest.validate_post_fields()`. (**views.py**)  
  - `has_object_permission()` → On PATCH, calls `UserRelatedRequest.validate_patch_fields()`. (**views.py**)  

---

## 2. Flow Diagram

    ```mermaid
    flowchart TD

        A[Incoming API Request] --> B{Request Method?}

        B -->|POST| C[HasUserPermission.has_permission]
        B -->|PATCH| D[HasUserPermission.has_object_permission]
        B -->|GET| E[UserRelatedRequest.get_queryset / AccessControl.get_response_fields]

        %% POST
        C --> C1[UserRelatedRequest.validate_post_fields]
        C1 --> C2[AccessControl.get_fields_for_post_request]
        C2 --> C3[AccessControl.is_admin?]
        C3 -->|Yes| C4[Return allowed fields from CSV]
        C3 -->|No| C5[Raise PermissionDenied]

        %% PATCH
        D --> D1[UserRelatedRequest.validate_patch_fields]
        D1 --> D2[AccessControl.get_fields_for_patch_request]
        D2 --> D3[AccessControl.get_most_privileged_perm_type]
        D3 --> D4[Return allowed fields from CSV]
        D4 --> D5[UserRelatedRequest.validate_request_fields]
        D5 -->|Disallowed fields?| D6[ValidationError]

        %% GET
        E --> E1[UserRelatedRequest.get_allowed_users]
        E1 --> E2[AccessControl.is_admin?]
        E2 -->|Yes| E3[Return all users]
        E2 -->|No| E4[Filter users by shared projects]
        E4 --> E5[AccessControl.get_response_fields → CSV permissions]
        E5 --> E6[Filter serializer output fields]

        %% Outcomes
        C5 --> F[403 PermissionDenied]
        D6 --> G[400 ValidationError]
        C4 & D5 & E6 --> H[Request Succeeds with Filtered Fields]
    ```

---

## 3. Sample CSV Permissions

Here’s a simple example of what the `FIELD_PERMISSIONS_CSV` might look like:

`table_name`,`field_name`,`get`,`post`,`patch`  
User,username,adminGlobal,adminGlobal,adminGlobal  
User,email,adminProject,adminGlobal,adminProject  
User,first_name,memberProject,adminProject,adminProject  
User,last_name,memberProject,adminProject,adminProject  
Project,name,adminProject,adminProject,adminProject  
Project,description,practiceLeadProject,adminProject,adminProject  

---

## 4. Summary

- **CSV-based permissions** define which fields are allowed per table, per operation (`get`, `post`, `patch`).  
- **AccessControl** enforces these rules.  
- **UserRelatedRequest** applies them to querysets, request data, and serializer output.  
- **HasUserPermission** ensures enforcement inside DRF request lifecycle.  

👉 This design provides **fine-grained field-level access control** and **context-aware user filtering** for secure multi-project environments.
