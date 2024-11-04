---
name: Update Table Issue
about: Describe this issue template's purpose here.
title: 'Update Table: [TABLE NAME]'
labels: 'feature: update table, good first issue, milestone: missing, role: back end,
  size: 0.25pt, stakeholder: missing'
assignees: ''

---

### Overview
We need to update the `TABLE_NAME` table model to [[reason goes here]]

#### Details
- The initial model issue: [[issue number]]

- Discussion leading to this change is here: [[issue number or link]]

### Action Items
- [ ] Update schema information
  - [ ] add/remove/alter given columns from [Entity Relationship Diagram (ERD)](https://lucid.app/lucidchart/ac2f3e81-00d2-4257-b1fc-266d7f0a4cbe/view)
  - [ ] add/remove/alter given columns from [PD: Table and Field definitions](https://docs.google.com/spreadsheets/d/1x_zZ8JLS2hO-zG0jUocOJmX16jh-DF5dccrd_OEGNZ0/edit#gid=1572339087)
  - [ ] make additional schema changes (if needed)
  - [ ] remove the ERD/SS update & db architect labels after these changes are made.
     - Permission is needed to edit the ERD and table spreadsheet.
- [ ] Update existing Django model
- [ ] Write a test for the new relationships this model will have with other models (e.g., creating a user and assigning them a set of permissions on a project) if any.
- [ ] Update API end point
- [ ] Update API unit tests
- [ ] Document the endpoint in Swagger

### Changes Needed
#### Columns to Remove
- [ ] Any columns that need to be deleted go here

#### Columns to Add
- [ ] Any columns that need to be added go here

#### Columns to Alter
- [ ] Any existing columns that need to be changed go here

#### Additional Changes
- These are usually changes to documentation rather than django

### Resources
- See [People Depot Resources wiki page](https://github.com/hackforla/peopledepot/wiki/Resources-and-Links) for links
  - ERD
  - Table and Field Definitions
  - API Endpoint
