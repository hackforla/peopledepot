Terminology:

- user row: a user row refers to a row being updated.  Row is redundant but included to
    help distinguish between row and field level security.
- team mate: a user assigned through UserPermissions to the same project as another user
- any project member: a user assigned to a project through UserPermissions
- general project member: a user assigned specifically as a project member to a project
- \[base configuration file\]\[base-field-permissions-reference\] - file used to configure
    screate, read, and update access for fields based on the factors listed below.

### Row Level Privileges

The following API endpoints retrieve users:

- api/v1/users: Create, read, and update user rows.  Global admins, can create, read, and update any user row.  Any project member can read any other project member.  Project leads can update any team mate.  Practice leads can update any
    team member in the same practice area.  When updating yourself, api/v1/me will provide greater
    permissions (global admins will have same permission)
- api/v1/me: Read and update your own row.  You can always read and update your own row.
- api/v1/self-register: Create a new user row without logging in.
- api/v1/eligible-users/<project id>?scope=\<all/team/notteam> - List users.  API is used by global admin or project lead **(\*)** when assigning a member to a team.  The separate API assigns the user to a project team is covered by a different document.

**(\*) Requirement for project lead needs to be verified with Bonnie**

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
