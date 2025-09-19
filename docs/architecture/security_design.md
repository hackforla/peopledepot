# Definition
- Requesting user: user making a request to perform an action on a target table record
- Related user: user that is associated with the target table record

# Security Roles
A user role is 
Security role is determined by comparing roles assigned to the requesting user, roles assigned
Rank and security roles used to determine if requesting user can
perform an operation are: 
6. None - no privilege
5. memberProject - project specific role.  Applicable if requesting
user is assigned memberProject and target user is assigned any role for the same project
4. practiceLeadProject - project and practice area role.  This role applies
3. adminProject,
2. adminBrigade 
1. adminGlobal

Lowest

# Field Security Configuration
Field security is configured in field_permissions.csv. For every table and field, this lists what is the minimum permission level required to get/patch/post that field. For instance,

```
User,first_name,memberProject,adminBrigade,adminGlobal
```

specifies that the first_name field in user requires memberProject or higher for get (view), adminBrigade for patch (update), and adminGlobal for post (create).

