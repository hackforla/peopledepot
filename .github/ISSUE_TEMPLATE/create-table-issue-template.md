---
name: Create Table issue template
about: Create an issue for each table required
title: 'Create Table: [name of table]'
labels: 'complexity: missing, feature: table creation, milestone: missing, role: back end, s: CTJ, s: hackforla.org, s: kb, s: tables, s: VRMS, size: 2pt'
assignees: ''
---

### Overview

We need to create the [ENTER NAME OF TABLE] table so that we can update a shared data store across hackforla.org, vrms, civictechjobs, and tables (onboarding) project.

#### Details

A table and a model are the same thing

### Action Items

- [ ] Identify if table has a description (see spreadsheet under Resources)
    - [ ] If not, reach out to PD leads
- [ ] Identify and document (below) what other tables are associated (see ERD under Resources)
- [ ] Create a single model in Django (defining schema)
- [ ] Write a test for the relationships this model will have with other models (e.g., creating a user and assigning them a set of permissions on a project).
- [ ] Write an API end point
- [ ] Write API unit tests
- [ ] Document the endpoint in Swagger

### Resources/Instructions

- See [People Depot Resources wiki page](https://github.com/hackforla/peopledepot/wiki/Resources-and-Links) for links
    - ERD
    - Table and Field Definitions
    - API Endpoint
- See [this Wiki page](https://github.com/hackforla/peopledepot/wiki/Create-Table-issues-data-gathering-workflow) for instructions on the data-gathering workflow for Create Table issues
- [ADD ANY OTHER RESOURCES/INSTRUCTIONS]

### Items to document (referenced above)

- [ADD ITEMS TO DOCUMENT]

#### Description

- [ENTER DESCRIPTION]

### Data Fields

- [ ] Copied from spreadsheet and confirmed according to ERD

| Name | Type | FK Table | FK Table Issue(s) |
| ---- | ---- | -------- | ----------------- |
| --   | --   | --       | --                |
| --   | --   | --       | --                |
| --   | --   | --       | --                |

- [ ] In ERD only (having items here indicates a mismatch, which requires a review)
    - None

### Associated Tables

1. Copied from spreadsheet and checked off according to ERD. (unchecked items indicate a mismatch between ERD and spreadsheet, which requires a review)

    - [ ] \[ENTER ASSOCIATED TABLE(S) with relation in brackets - e.g., `(one-to-many)`\]

1. In ERD only (having items here indicates a mismatch, which requires a review)

    - None

#### Swagger Endpoint Link

- [ADD SWAGGER ENDPOINT LINK]
