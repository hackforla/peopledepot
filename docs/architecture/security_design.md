Security is derived from field_permissions.csv. For every table and field, this lists what is the minimum permission level required to get/patch/post that field. For instance,

```
User,first_name,memberProject,adminBrigade,adminGlobal
```

specifies that the first_name field in user requires memberProject or higher for get (view), adminBrigade for patch (update), and adminGlobal for post (create).

Permission levels are: None, memberProject, practiceLeadProject, adminProject, adminBrigade, adminGlobal
