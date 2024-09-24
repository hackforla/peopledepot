Terminology:

- user row: a user row refers to a row being updated.  Row is redundant but included to
    help distinguish between row and field level security.
- team mate: a user assigned through UserPermission to the same project as another user
- any project member: a user assigned to a project through UserPermission
- API end points / data operations
    - get / read
    - patch / update
    - post / create

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
                "user_field_permissions\[admin_global\]").
            - Project leads can read and update fields of a target team member specified in
                \[base_user_cru_constants.py\] for project lead (search for (search for
                "user_field_permissions\[admin_project\]") .
        - If a practice area admin is associated with the same practice area as a target
            fellow team member, the practice area admin can read and update fields
            specified in \[base_user_cru_constants.py\] for practice area admin (search for "user_field_permissions\[practice_lead_project\]").  Otherwise, the practice admin can read
            fields specified in \[base_user_cru_constants.py\] for project team member (search
            for "user_field_permissions\[member_project\]")

    - General project team members can read fields for a target fellow team member specified in \[base_user_cru_constants.by\] for project team member (search for "user_field_permissions\[member_project\]")

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

#### End Point Technical Implementation

- /user
    - response fields for get, patch, and post: `UserSerializer.to_representation` => `PermissionCheck.get_user_read_fields` determines which fields are serialized.\
        **serializers.py, permission_check.py**
    - read
        - /user - see above bullet about response fields.  No processing on incoming request as no request fields to process.
        - /user/<uuid> fetches a specific user.  See above bullet about response fields.  If the requester does not have permission
            to view the user, PermisssionUtil.get_user_read_fields will find no fields to serialize and throw a ValidationError.
    - patch (update): `UserViewSet.partial_update` => `PermissionCheck.validate_patch_request(request)` => `PermissionCheck.PermissionCheck.validate_fields_patchable(requesting_user, target_user, request_fields)` will check field permission logic for request fields.  If the request fields
        include a field outside the requester's scope, the method returns a PermissionError, otherwise the
        record is udated.  **views.py, permission_check.py**
    - post (create): UserViewSet.create: If the requester is not a global admin, the create method
        will throw an error.  **views.py**
- /me
    - response fields for get and patch: `UserProfileAPISerializer.to_representation` => `PermissionCheck.get_user_read_fields` determines which fields are serialized.
    - get: see response fields above.  No request fields accepted.  **views.py, serializer.py**
    - patch (update): By default, calls super().update_partial of UserProfileAPIView for
        the requesting user to update themselves.  **views.py, serializer.py**
    - post (create): not applicable.  Prevented by setting http_method_names in
        UserProfileAPIView to \["patch", "get"\]
- /self-register (not implemented as of July 9, 2024):
    - read: N/A.  Prevented by setting http_method_names in
        SelfRegisterView to \["post"\]
    - patch (update): N/A.  Prevented by setting http_method_names in
        SelfRegisterView to \["post"\]
    - post (create): SelfRegisterView.create => PermissionCheck.validate_self_register_postable

#### Supporting Files

Documentation is generated by pydoc package.  pydoc reads comments between triple quotes. See \[Appendix A\]

- [permission_check.html](./docs/pydoc/permission_check.html)
- [permission_fields.py](./docs/pydoc/field_permissions.html) => called from permission_check to
    determine permissiable fields.  permission_fields.py derives permissable fields from
    user_permission_fields.
- user_permission_fields_constants.py => see permission_fields.py
- constants.py => holds constants for permission types.
- urls.py

### Test Technical Details

Details of the purpose of each test and supporting code can be found in the the docs/pydoc documentation.  Additional methods are automatically called based on the name
of the method.

django_db_setup in conftest.py is automatically called before any test is executed.
This code populates seed data for tests.  Workflow of code is as follows:
django_db_setup => call("load_command") => Command.handle class method in directory
tests/management/command => SeedUser.create_data and SeedCommand.load_data class method

### Appendix A - Generate pydoc Documentation

#### Adding New Documentation

pydoc documentation are located between triple quotes.

- See https://realpython.com/documenting-python-code/#docstring-types for format for creating class, method,
    or module pydoc.  For documenting specific variables, you can do this as part of the class, method,
    or module documentation.
- Check the file is included in documentation.py
- After making the change, generate as explained below.

#### Modifying pydoc Documentation

Look for documentation between triple quotes.  Modify the documentation, then generate as explained
below.

#### Generating pydoc Documentation

From Docker screen, locate web container.  Select option to open terminal.  To run locally, open local
terminal.  From terminal:

```
cd app
../scripts/loadenv.sh
python documentation.py
mv *.html ../docs/pydoc
```
