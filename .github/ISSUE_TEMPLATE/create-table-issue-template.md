---
name: Create Table issue template
about: Create an issue for each table required
title: 'Create Table: [name of table]'
labels: 'complexity: missing, feature: table creation, milestone: missing, role: back
  end, s: CTJ, s: hackforla.org, s: kb, s: tables, s: VRMS, size: 2pt'
assignees: ''

---

### Overview

We need to create the \[name of table\] table so that we can update a shared data store across hackforla.org, vrms, civictechjobs, and tables (onboarding) project.

#### Details

A table and a model are the same thing

### Action Items

- [ ] identify if table has a description (see spreadsheet under Resources)
    - [ ] if not, reach out to PD leads
- [ ] identify and document  (below) what other tables are associated (see ERD under Resources)
- [ ] create a single model in Django (defining schema)
- [ ] Write a test for the relationships this model will have with other models (e.g., creating a user and assigning them a set of permissions on a project).
- [ ] Write an API end point
- [ ] write API unit tests
- [ ] Document the endpoint in Swagger

### Resources/Instructions

- See [People Depot Resources wiki page](https://github.com/hackforla/peopledepot/wiki/Resources-and-Links) for links

### Items to document (referenced above)

#### Description

-

#### Associated Tables

-

#### Swagger Endpoint Link

-
