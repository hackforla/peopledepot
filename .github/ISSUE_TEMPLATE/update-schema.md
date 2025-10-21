---
name: Update Schema
about: To be created alongside an "Update Table" issue
title: 'Update Schema: [TABLE NAME]'
labels: 'complexity: small, dependency, feature: ERD/SS adjustment, milestone: missing,
  role: db architect, s: PD team, size: 0.25pt, stakeholder: missing'
assignees: ''

---

### Dependency

- [ ] Update Table issue: #[Replace with ISSUE NUMBER]

### Overview

Changes need to be made to the spreadsheet and the ERD to reflect the changes made to the [TABLE NAME] model (code), so that all three can be consistent.

### Action Items

- Make changes listed below in the ERD (can be done before or after code updates)
    - [ ] Fields have been removed (if needed)
    - [ ] Fields have been added (if needed)
    - [ ] Fields have been Updated (if needed)
    - [ ] Additional schema changes have been made (if needed)
- (after the code has been changed) Make changes to spreadsheet so that the following columns are all the same (this should make the value in "Is the code the same as the plan?" have the value of TRUE
    - [ ] Called in code
    - [ ] New Field Name
    - [ ] Field Name

### Changes Needed

#### Fields to Remove

- [ ] Any fields that need to be deleted go here. Remove this section if unused

#### Fields to Update

Any existing columns that need to be changed are added to the table below (ex: name changes, type changes). Remove this section if unused

#### Fields to Add

- [ ] Any fields that need to be added go here. Remove this section if unused

#### Additional Changes

- List any changes that are not field changes here (ex: relationship changes, table name changes, additional information added to the ERD). Remove this section if unused

### Resources

- [Entity Relationship Diagram (ERD)](https://lucid.app/lucidchart/ac2f3e81-00d2-4257-b1fc-266d7f0a4cbe/view)
- [PD: Table and field explanations, Field Permissions](https://docs.google.com/spreadsheets/d/1x_zZ8JLS2hO-zG0jUocOJmX16jh-DF5dccrd_OEGNZ0/edit?gid=371053454#gid=371053454)
