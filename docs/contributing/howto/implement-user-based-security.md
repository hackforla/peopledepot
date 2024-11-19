# Terminology

**one-to-many user-related data access policy:** policy for tables where each row in the table is related to one and only one user, directly or indirectly.
**authorization data access policy:** policy that requires authorization for create, update, delete and optionally read access.\
**other data access policy:** any custom policy not covered by the previous two polices.  For example, data access policy for create, update, and delete could be based on Djano roles.  In that scenario, a specific table might only be updateable by a user with a specific Django role.

# One-to-many user related data policy

## user field

A table that uses a user related data policy must have "user" as a field that references the one user for a particluar row.

## Fetching Rows

- determines which rows are returned for a get request
- implementation:
    modify views.py
    - find <table>ViewSet
    - add the following code:

```
      def get_queryset(self):
        queryset = GenericRequest.get_queryset(view=self)
```

## Record security

- determines whether a specific record can be viewed, updated, or created.  If the table requires field level security then implementing record level security is not required.
- implementation:
    - modify views.py
        - find <table>ViewSet
        - find line `permission = [....]`
        - add UserBasedRecordPermission to the list

## Field security

- determines which fields, if any, can be included in a request to update or create.
- implementation:
    - modify field_permissions.csv to include field level configuration, if not already there
    - modify views.py
        - find <table>ViewSet
        - find line `permission = [....]`
        - add UserBasedFieldPermission to the list

## Response data

- determines the fields returned in a response for each row.
- implementation:
    - modify serializer.py
        - find <table>Serializer
        - add following code at end of serializer:

```
def to_representation(self, instance):
    representation = super().to_representation(instance)
    return GenericRequest.get_serializer_representation(self, instance, representation)
```

# Authorization data access policy

For many tables, create, update, and delete for all rows in the table are allowed if the request is from an authenticated user.  Ability to read all rows may or may not require authentication.  To implement one of these
options modify view.py:

- find <table>ViewSet
- find line `permission = [....]`
- if read access requires authentication, make sure the permission includes isAuthenticated
- if read access does not require authentication, add isAuthenticatedOrReadOnly and if applicable, remove isAuthenticated.

# Appendix A - Notes on API endpoints

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
