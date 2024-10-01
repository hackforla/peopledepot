### Terminology

- user row: a user row refers to a row being updated.  Row is redundant but included to
    help distinguish between row and field level security.
- team mate: a user assigned through UserPermission to the same project as another user
- any team member: a user assigned to a project through UserPermission
- API end points / data operations
    - get / read
    - patch / update
    - post / create

### Functionality

#### Field level specifics / cru.py

The implemented field level security specifics can be derived from [cru.py](../../app/core/cru.py) and should match the requirements.  If requirements change or the requirements
don't match what is implemented then this file needs to change.

The descriptions of end points below will describe where the specifics are implented in cru.py.

#### /users endpoint

- Row level security

    - Functionality: Global admins, can create, read,
        and update any user row.  Any team member can read any other project member.  Project leads can update any team member.  Practice leads can update any team member in the same practice area (not currently implemented)

- Field level security:

    - /user end point:
        - Global admins can read, update, and create fields specified by
            \_cru_permissions\[admin_global\] in [cru.py](../../app/core/cru.py).

        - Project admins can read and update fields specified in
            [cru.py](../../app/core/cru.py) for fellow team members.\
            Search for for `user_assignment_field_cru_permissions[admin_project]` in
            constants file.

        - Practice area leads can read and update fields specified specified by
            `_cru_permissions[practice_lead_project]` in
            [cru.py](../../app/core/cru.py) for fellow team members in the same
            practice area.  If the team member is in a different practice area,
            the project lead can read fields specified by  `_cru_permissions[member_project]` in
            [cru.py](../../app/core/cru.py).

            Note: As of 24-Sep-2024, the implemented code treats practice area leads the same as project admins.

        - Project team members can read fields specified by  for fellow team members.

#### /me endpoint

Used for reading and updating information about yourself when you are logged in.

- Row Level Security: Logged in user can always read and update their own information
- Field Level Security: When using the me endpoint, the read and update fields are
    specificed \`\_gitrcru_permissions\[profile_value\] in [cru.py](../../app/core/cru.py)

#### /self-register endpoint

As of 26-Sep-2024, this feature is not implemented and not documented in detail.

Create a new user row without logging in.  For field permissions, search for "self_register_permissions" in
`[user_assignment_field_cru_permissions.py]`

#### /eligible-users/<project id>?scope=\<all/team/notteam> - List users.

API is used by global admin or project lead **(\*)** when assigning a user to a team.

As of 26-Sep-2024, this feature is not implemented.  When implemented, the API wll let
global and project admins read fields  specified in \`cru_permissions\[member_project\]
in [cru.py](../../app/core/cru.py).

### Technical implementation

#### End Point Technical Implementation

- /user
    - response fields for get, patch, and post:
        **serializers.py, permission_check.py**
    - get (read)
        - get `to_representation` method for class UserSerializer calls => `PermissionCheck.get_user_read_fields` determines which fields are serialized.\\
    - patch (update): `UserViewSet.partial_update` => `PermissionCheck.validate_patch_request(request)` => `PermissionCheck.PermissionCheck.validate_fields_patchable(requesting_user, target_user request_fields)` will check field permission logic for request fields based on the requesting
        user and taget user.  If the request fields include a field outside the requester's scope, the method returns a PermissionError, otherwise the record is updated.  **views.py, permission_check.py**
    - post (create): UserViewSet.create: If the requester is not a global admin, the create method
        will throw an error.  If the fields specified in the request are out of scope, the
        method returns an error.  **views.py**
- /user/<uuid> fetches a specific user.
    - get (read) Get is the only method that applies.  Fetches a specific user.  See above bullet about response fields.  If the requester does not have permission
        to view the user, PermisssionUtil.get_user_read_fields will find no fields to serialize and throw a ValidationError. See above bullet about response fields.  If the requester does not have permission
        to view the user, PermisssionUtil.get_user_read_fields will find no fields to serialize and throw a ValidationError.
- /me
    - response fields for get and patch: `UserProfileAPISerializer.to_representation` => `PermissionCheck.get_user_read_fields` determines which fields are serialized.
    - get: see response fields above.  No request fields accepted.  **views.py, serializer.py**
    - patch (update): By default, calls super().update_partial of UserProfileAPIView for
        the requesting user to update themselves.  **views.py, serializer.py**
    - post (create): not applicable.  Prevented by setting http_method_names in
        UserProfileAPIView to \["patch", "get"\]
- /self-register (not implemented as of July 9, 2024):
    \*\* views.py, serializer.py
    - read: N/A.  Prevented by setting http_method_names in
        SelfRegisterView to \["post"\]
    - patch (update): N/A.  Prevented by setting http_method_names in
        SelfRegisterView to \["post"\]
    - post (create): SelfRegisterView.create => PermissionCheck.validate_self_register_postable
        `UserProfileAPISerializer.to_representation` => `PermissionCheck.get_user_read_fields` determines which fields are serialized.
    - get: see response fields above.  No request fields accepted.  **views.py, serializer.py**

#### Supporting Files

Documentation is generated by pydoc package.  pydoc reads comments between triple quotes. See \[Appendix A\]

- [permission_check.html](./docs/pydoc/permission_check.html)
- [permission_fields.py](./docs/pydoc/http_method_field_permissions.html) => called from permission_check to
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
