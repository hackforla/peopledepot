### Terminology:

- user row: a user row refers to a row being updated.  Row is redundant but included to
    help distinguish between row and field level security.
- team mate: a user assigned through UserPermission to the same project as another user
- any team member: a user assigned to a project through UserPermission
- API end points / data operations
    - get / read
    - patch / update
    - post / create

### Source of Privileges

Field level security specifics are derived from u[cru.py](../../app/core/cru_permissions.py).  The file includes several lists that
you can use to derive different privileges.  Search for these terms

- `_cru_permissions[profile_value]`
- `_cru_permissions[member_project]`
- `_cru_permissions[practice_lead_project]`
- `_cru_permissions[admin_global]`
    fields followed by CRU or a subset of CRU for Create/Read/Update.  Example:
    `first_name:["RU"]` for a list would indicate that first name is readable and updateable
    for the list.

### Functionality

The following API endpoints retrieve users:

#### /users endpoint functionality

- Row level security

    - Functionality:
        - Global admins, can create, read, and update any user row.
        - Any team member can read any other project member.
        - Project leads can update any team member.
        - Practice leads can update any team member in the same practice area (not currently implemented)

- Field level security:

    - /user end point:
        - Global admins can read, update, and create fields specified in
            [cru.py](../../app/core/cru.py).  Search for
            `_user_permissions[admin_global]`).

        - Project admins can read and update fields specified in
            [cru.py](../../app/core/cru.py) for other project leads.\
            Search for for `_user_permissions[admin_project]` in [cru.py](../../app/core/cru.py)

        - Practice area leads can read and update fields specified in
            [cru.py](../../app/core/cru.py) for fellow team members.  If
            the team member is in the same practice area,\
            Search for for `_user_permissions[practice_lead_project]` in [cru.py](../../app/core/cru.py)

            If user being queried is not from the same practice area then search for `_user_permissions[member_project]`

            Note: As of 24-Sep-2024, the implemented code treats practice area leads the same as project
            admins.

        - Project members can read fields specified in
            [cru.py](../../app/core/cru.py) for fellow team members.
            Search for for `_user_permissions[member_project]` in [cru.py](../../app/core/cru.py)

    Note: for non global admins, the /me endpoint, which can be used when reading or
    updating yourself, provides more field permissions.

#### /me endpoint functionality

Used for reading and updating information about the user that is logged in.  User permission assignments do not apply.

- Row Level Security: Logged in user can always read and update their own information.
- Field Level Security: For read and update permissions, see `_cru_permissions[profile_value]` in [cru.py](../../app/core/cru.py).

#### /eligible-users/<project id>?scope=\<all/team/notteam> - List users.

This is covered by issue #394.

#### End Point Technical Implementation

##### Field level specifics / cru.py

The implemented field level security specifics can be derived from [cru.py](../../app/core/cru.py) and should match the requirements.  If field privileges change or the requirements
don't match what is implemented this can be fixed by changing [cru.py](../../app/core/cru.py).

##### /user endpoint technical implementation

- response fields for get, patch, and post:
    **serializers.py, permission_check.py**
- get (read)
    - /user - see above bullet about response fields.
    - /user/<uuid> fetches a specific user.  See above bullet about response fields.  If the requester does not have permission
        to view the user, PermisssionUtil.get_user_read_fields will find no fields to serialize and throw a ValidationError
- patch (update): `UserViewSet.partial_update` => `PermissionCheck.validate_patch_request(request)`.\
    validate_fields_patchable(requesting_user, target_user, request_fields)\` will compare request fields
    against `cru.user_post_fields[admin_global]` which is derived from `_cru_permissions`.  If the request fields
    include a field outside the requester's scope, the method returns a PermissionError, otherwise the
    record is udated.  **views.py, permission_check.py**
- post (create): UserViewSet.create: If the requester is not a global admin, the create method
    will throw an error. Calls PermissionCheck.validate_fields_postable which compares
    pe **views.py**

##### /me end point technical implementation

- response fields for get and patch: `UserProfileAPISerializer.to_representation` => `PermissionCheck.get_user_read_fields` determines which fields are serialized.
- get: see response fields above.  No request fields accepted.  **views.py, serializer.py**
- patch (update): By default, calls super().update_partial of UserProfileAPIView for
    the requesting user to update themselves.  **views.py, serializer.py**
- post (create): not applicable.  Prevented by setting http_method_names in
    UserProfileAPIView to \["patch", "get"\]

#### Supporting Files

Documentation is generated by pydoc package.  pydoc reads comments between triple quotes. See Appendix A.

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
python scripts/
documentation.py
mv *.html ../docs/pydoc
```
