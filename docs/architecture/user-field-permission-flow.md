Terminology:

- user row: a user row refers to a row being updated.  Row is redundant but included to
    help distinguish between row and field level security.
- team mate: a user assigned through UserPermissions to the same project as another user
- any project member: a user assigned to a project through UserPermissions
- general project member: a user assigned specifically as a project member to a project
- [base configuration file][base-field-permissions-reference] - file used to configure
    screate, read, and update access for fields based on the factors listed below.

### Functionality

The following API endpoints retrieve users:

- /users:

    - Row level security

        - Functionality: Global admins, can create, read,
            and update any user row.  Any project member can read any other project member.  Project leads can update any team mate.  Practice leads can update any team member in the same practice area.

    - Field level security:

        \[base_user_cru_constants.py\] is used for field permissions and is based on rules
        sspecified elsewhere.  If the rules change, then \[base_user_cru_constants\] must change.

        - /user end point:
            **/user end point**
            - Global admins can read, update, and create fields specified in
                \[base_user_cru_constants.py\] for global admin (search for
                "user_field_permissions\[global_admin\]").
            - Project leads can read and update fields of a target team member specified in
                \[base_user_cru_constants.py\] for project lead (search for (search for
                "user_field_permissions\[project_lead\]") .
        - If a practice area admin is associated with the same practice area as a target
            fellow team member, the practice area admin can read and update fields
            specified in \[base_user_cru_constants.py\] for practice area admin (search for "user_field_permissions\[practice_area_admin\]").  Otherwise, the practice admin can read
            fields specified in \[base_user_cru_constants.py\] for project team member (search
            for "user_field_permissions\[project_member\]")

    - General project team members can read fields for a target fellow team member specified in \[base_user_cru_constants.by\] for project team member (search for "user_field_permissions\[project_member\]")

    Note: for non global admins, the /me endpoint, which can be used when reading or
    updating yourself, provides more field permissions.

    - /me: Read and update yourself.  For read and update field permissions, search for
        "me_endpoint_permissions" in \[base_user_cru_constants.py\].

\[base_user_cru_constants.py\] for the me url (search for "me_endpoint_permissions")

- api/v1/self-register: Create a new user row without logging in.  For field permissions, search
    for "self_register_permissions"
- api/v1/eligible-users/<project id>?scope=\<all/team/notteam> - List users.  API is used by global admin or project lead **(\*)** when assigning a user to a team.  This API uses the same
    read fiel permissions as specified for /user end point for project team members (search for
    "user_field_permissions\[project member\]").
    A separate API for assigning the user to a project team is covered by a different document.

**(\*) Requirement for project lead needs to be verified with Bonnie**

### Technical implementation

- /user
    - response fields: for all methods are determined by to_representation method in
        UserSerializer in serializers.py.  The method calls PermissionUtil.get_lowest_ranked_permission_type
    - read
        - /user fetches rows using the get_queryset method in the UserViewSet from views.py.
        - /user/<uuid> fetches a specific user.  If a requester tries to fetch a user outside
            their permissions, the to_representation method of UserSerializer will determine there are no eligible response fields and will throw an error.
        - see first bullet for response fields returned.
    - patch (update): field permission logic for request fields is controlled by
        partial_update method in UserViewset.  See first bullet for response fields returned.
    - post (create): field permission logic for allowable request fields is controlled by the create method in UserViewSet.  If a non-global admin uses this method the create method
        will throw an error.
- /me
    - read: fields fetched are determined by to_representation method in UserProfileSerializer
    - patch (update): field permission logic for request fields is controlled by
        partial_update method in UserProfileViewSet.
    - post (create): not applicable.  Prevented by setting http_method_names in
        UserProfileViewSet to \["patch", "get"\]
- /self-register (not implemented as of July 9, 2024):
    - read: N/A.  Prevented by setting http_method_names in
        UserProfileViewSet to \["patch", "get"\]
    - patch (update): N/A.  Prevented by setting http_method_names in
        UserProfileViewSet to \["patch", "get"\]
    - post (create): field permission logic for allowable request fields is
        controlled by the create method in SelfRegisterViewSet.

### Field Level Permissions

If a user has create, read, or update privileges for a user row, the specific fields
that can be updated are configured through the

### users end point

This section covers security when creating, reading, or updating a user row using the api/v1/susers endpoint.  If reading or updating yourself you will have either more or the same privileges using the api/v1/me endpoint.  If you are creating an account for yourself when none existed, see the api/v1/self-register endpoint.

#### Read and Update

For the api/v1/users end point, the fields a requester can read or update of a target user
(if any) are based on the following factors

- if the requester is a global admin, then the requester can read and update any user row.\
    The specific fields tht are readable or updateable are configured in the file

[base-field-permissions-reference]: ../../app/core/base_user_cru_constants.py
