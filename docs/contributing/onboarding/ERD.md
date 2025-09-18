# Updating the ERD

This page outlines how to **view**, **edit**, and **propose changes** to the People Depot entity relationship diagram (ERD), which is managed using [dbdiagram.io](https://dbdiagram.io/).

## 📌 Purpose

To ensure database schema edits are **collaborative**, **auditable**, and **synchronized with the source of truth**, all edits must go through GitHub via a structured process described below.

## 🔍 Viewing the Live ERD

To view the current version of the ERD:

- Visit: **Live ERD (dbdiagram.io)** → [link](https://dbdiagram.io/d/People-Depot-Schema-ERD-68917d4edd90d178656e4061)

!!! note

    📝 You do **not** need an account to view the ERD

## ✏️ How to Propose Changes to the ERD

All edits must be submitted via pull request using the steps below.

1. Fork the Repository

    1. Navigate to the People Depot GitHub repo
    1. Click **Fork**

    !!! note

        Ensure your fork is up-to-date before making changes

1. Copy the Schema Source

    1. Locate the file: `schema.dbml` in the root folder
    1. Copy the **entire contents** of the file

1. Make edits on dbdiagram.io (Your Account)

    1. Sign in to [dbdiagram.io](https://dbdiagram.io/) using **your own free account**
    1. Create a **new diagram**
    1. Paste the contents of `schema.dbml` into the editor
    1. Make your proposed changes using [DBML syntax](https://dbml.dbdiagram.io/docs/)
    1. Ensure the diagram renders correctly

1. Export Updated Schema

    - Once edits are complete and validated visually:
        1. Click **Export**
        1. Choose **DBML**
        1. Save the file as `schema.dbml`

1. Commit & Push Changes

    - In your forked repo:
        1. Replace the original `schema.dbml` file with your updated version
        1. Commit your changes with a descriptive message (e.g., `Add table for program milestones`)
        1. Push to your fork

1. Submit a Pull Request

    1. Open a PR from your fork to the `main` branch of `PeopleDepot`
    1. Title your PR descriptively (e.g., `Update ERD to include new Program table`)
    1. In the PR body, explain:
        1. What you changed
        1. Why you changed it
        1. Anything reviewers should double-check (e.g., table relationships, naming consistency)

## ✅ After Your PR Is Merged

Once your PR is approved and merged:

1. A maintainer will manually **update the official ERD** on dbdiagram.io under the `PeopleDepot@hackforla.org` account using your submitted `schema.dbml` file.
1. The Live ERD link will reflect your changes shortly after.

!!! note

    You will **not** be given access to the shared dbdiagram.io account.

    All official updates are uploaded by maintainers.

---

## 🛠 Tips and Conventions

- Use **clear, singular table names** (e.g., `Person`, not `People`)
- Always define **primary keys** and **foreign keys**
- Maintain consistent **naming conventions** (e.g., `snake_case` or `camelCase`, as established)
- Include **comments in DBML** for any complex relationships or logic

---

## 🧠 Resources

- 📖 [DBML Syntax Reference](https://dbml.dbdiagram.io/docs/)
- 📘 [ERD Best Practices](https://www.lucidchart.com/pages/er-diagram-symbols-and-meaning)
