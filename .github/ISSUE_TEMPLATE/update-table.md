---
name: Update Table
about: Describe this issue template's purpose here.
title: 'Update Table: [TABLE NAME]'
labels: 'feature: update table, good first issue, milestone: missing, role: back end,
  size: 0.25pt, stakeholder: missing'
assignees: ''

---

### Overview
We need to update the [Replace with TABLE NAME] table model to [Replace with REASON]

#### Details
- The initial model issue: #[Replace with ISSUE NUMBER]
- Discussion leading to this change is here: [Replace with ISSUE URL OR OTHER LINK]

### Action Items
- [ ] Update existing Django model
  - [ ] In the files indicated by Resource 1.01, Change the following items in the code
   ```
   [Replace with UPDATE TABLE]
   ```
  - [ ] Add the following items in the code
   ```
   [Replace with ADD TABLE]
   ```
- [ ] Write a test for the new relationships this model will have with other models (e.g., creating a user and assigning them a set of permissions on a project) if any.
- [ ] Update API end point
- [ ] Update API unit tests
- [ ] Document the endpoint in ReDocs

### Resources
- 1.01 Code locations
   - 1.01.01 https://github.com/hackforla/peopledepot/blob/main/app/core/models.py
   - 1.01.02 https://github.com/hackforla/peopledepot/blob/main/app/core/admin.py
   - 1.01.03 https://github.com/hackforla/peopledepot/blob/main/app/core/api/serializers.py
   - 1.01.04 https://github.com/hackforla/peopledepot/blob/main/app/core/migrations/0002_user_current_job_title_user_current_skills_and_more.py
- 1.02 [People Depot Resources wiki page](https://github.com/hackforla/peopledepot/wiki/Resources-and-Links) for links
  - ERD
  - Table and Field Definitions
  - API Endpoint
