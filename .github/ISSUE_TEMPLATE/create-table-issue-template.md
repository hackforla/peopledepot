---
name: Create Table issue template
about: Create an issue for each table required
title: 'Create Table: [name of table]'
labels: 'complexity: missing, feature: table creation, milestone: missing, role: back
  end, s: CTJ, s: hackforla.org, s: kb, s: tables, s: VRMS, size: 2pt'
assignees: ''

---

### Overview

We need to create the [ADD NAME OF TABLE] table so that we can update a shared data store across hackforla.org, vrms, civictechjobs, and tables (onboarding) project.

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

- [ADD DESCRIPTION]

### Data Fields

- [ ] Copied from spreadsheet and confirmed according to ERD

| Name | Type | FK Table | FK Table Issue(s) |
| ---- | ---- | -------- | ----------------- |
| --   | --   | --       | --                |
| --   | --   | --       | --                |
| --   | --   | --       | --                |

- [ ] In ERD only (having items here indicates a mismatch, which requires a review)

    - None [or REPLACE WITH FIELD NAME - TYPE]

- Check to see if open issues in `FK status` below

    - [ ] If all Issues listed are closed (or there are no FKs), then skip the next 3 steps
        - [ ] comment out the code after you create it (see FK Status below for open/closed state)
        - [ ] add an action item on the open issue to uncomment the code line you commented out when that issue's table is created.
        - [ ] Provide your file and line number as a permalink under resources in that issue

### FK status

- [#ISSUE NUMBER OF ANY FK TABLE(S)]

### Associated Tables

1. Copied from spreadsheet and checked off according to ERD. (unchecked items indicate a mismatch between ERD and spreadsheet, which requires a review)

    - [ ] \[ENTER NAME OF ASSOCIATED TABLE, relation in brackets (e.g., `(one-to-many)`), and #issue number\]

1. In ERD only (having items here indicates a mismatch, which requires a review)

    - None

#### Swagger Endpoint Link

- [ADD SWAGGER ENDPOINT LINK]
