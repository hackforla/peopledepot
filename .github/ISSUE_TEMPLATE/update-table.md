---
name: Update Table
about: Describe this issue template's purpose here.
title: 'Update Table: [TABLE NAME]'
labels: 'feature: update table, good first issue, milestone: missing, role: back end,
  size: 0.25pt, stakeholder: missing'
assignees: ''

---

### Overview

We need to update the [Replace with TABLE NAME] table model to [Replace with REASON, possibly "to include new fields and have the correct names for fields."]

#### Details

- The initial model issue: #[Replace with ISSUE NUMBER]
- Discussion leading to this change is here: [Replace with ISSUE URL OR OTHER LINK OPTIONAL]

### Action Items

- Update existing Django model

- [ ] In the files indicated by Resource 1.01, Change the following items in the code

| Current Name in code | Updated Name | Updated Type (may already be this type) | FK Table | FK Table Issue(s) |
| -------------------- | ------------ | --------------------------------------- | -------- | ----------------- |
| --                   | --           | --                                      | --       | --                |

- [ ] Add the following items in the code

| Name | Type | FK Table | FK Table Issue(s) |
| ---- | ---- | -------- | ----------------- |
| --   | --   | --       | --                |

- Check to see if open issues in `FK status` below

    - [ ] If all Issues listed are closed (or there are no FKs), then skip the next 3 steps
        - [ ] comment out the code after you create it (see FK Status below for open/closed state)
        - [ ] add an action item on the open issue to uncomment the code line you commented out when that issue's table is created.
        - [ ] Provide your file and line number as a permalink under resources in that issue

- [ ] Write a test for the new relationships this model will have with other models (e.g., creating a user and assigning them a set of permissions on a project) if any.

- [ ] Update API end point

- [ ] Update API unit tests

- [ ] generate a schema table description (see resources 1.04), post it in a comment below, and add a link to it in the Update Schema dependency issue

- [ ] Document the endpoint in ReDocs (see resources 1.05)

### FK status

- [#ISSUE NUMBER OF ANY FK TABLE(S)]

### After PR has been approved

- [ ] Release the dependency and move the issue out of the icebox for [Replace with ISSUE NUMBER OF UPDATE ERD]

### Resources

- 1.01 Code locations
    - 1.01.01 [/app/core/models.py](https://github.com/hackforla/peopledepot/blob/main/app/core/models.py)
    - 1.01.02 [/app/core/admin.py](https://github.com/hackforla/peopledepot/blob/main/app/core/admin.py)
    - 1.01.03 [/app/core/api/serializers.py](https://github.com/hackforla/peopledepot/blob/main/app/core/api/serializers.py)
    - 1.01.04 [/app/core/api/views.py](https://github.com/hackforla/peopledepot/blob/main/app/core/api/views.py)
- 1.02 [People Depot Resources wiki page](https://github.com/hackforla/peopledepot/wiki/Resources-and-Links) for links
    - ERD
    - Table and Field Definitions
    - API Endpoint
- 1.03 Spreadsheet: [PD: Table and field explanations, Field Permission tab](https://docs.google.com/spreadsheets/d/1x_zZ8JLS2hO-zG0jUocOJmX16jh-DF5dccrd_OEGNZ0/edit?gid=371053454#gid=371053454)
    -1.03.01 [ADD A LINK TO A SPECIFIC FILTER FOR THE TABLE]
- 1.04 [Instructions for how to generate a schema table description](https://hackforla.github.io/peopledepot/contributing/howto/generate-db-table-description/)
- 1.05 [Instructions for how to Document End point](https://hackforla.github.io/peopledepot/contributing/howto/add-model-and-api-endpoints/#add-viewset) step 3
