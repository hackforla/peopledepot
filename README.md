[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)

# PeopleDepot

PeopleDepot is a project of Hack for LA/Civic Tech Structure Inc. 501(c)(3). PeopleDepot aims to provide a single source of truth as the backend infrastructure and data store for Hack for LA projects, including data about people, program areas, and projects. PeopleDepot uses PostgreSQL for its database and Django as the backend data model framework with Django REST Framework for the API layer. PeopleDepot's goal is to serve as a repository of information for other infrastructure projects (e.g., VRMS, Hack for LA Website, Civic Tech Index, Tables, etc).

## Project context

The hardest part about running a large organization using only free or open source tools and technologies is how to manage the flow of information and provide relevant info to all the people and projects that need it. Managing multiple databases inefficiently can end up taking more time than the projects themselves. This project seeks to create a maintainable database infrastructure that is synchronized.

In the process, it should allow for further automation and do away with manual storage of duplicate information across projects, which includes:

- Recruiting members (Website: Project info and meeting times)
- Onboarding members to resources (e.g., GitHub, Google Calendar, Google Drive, Google Docs, Google Sheets, etc.)
- Helping members find roles (Civic Tech Jobs: roles and project info)
- Managing team permissions (VRMS: GitHub, Google Calendar, Google Drives, etc.)

## Technology used

- [Docker][docker-docs]
- [Django][django-docs]
- [DjangoRestFramework][drf-docs]
- [PostgreSQL][postgres-docs]

## How to contribute

1. Join our organization by going through [Hack for LA Onboarding][hfla onboarding]. It's free to join!
1. Read the [onboarding section of our Wiki](https://github.com/hackforla/peopledepot/wiki/Developer-Onboarding).
1. Read our [Contributing Guidelines][contributing] and follow the instructions there.

## Contact info

Contact us in the `#people-depot` channel on Slack.

## Licensing

This repository uses the [GNU General Public License (v2.0)][licensing].

<!-- References section -->

[contributing]: http://hackforla.github.io/peopledepot/contributing/
[django-docs]: https://docs.djangoproject.com/
[docker-docs]: https://www.postgresql.org/docs/
[drf-docs]: https://www.django-rest-framework.org/tutorial/quickstart/
[hfla onboarding]: https://www.hackforla.org/getting-started
[licensing]: ./LICENSE
[postgres-docs]: https://www.postgresql.org/docs/
