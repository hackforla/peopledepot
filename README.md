[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)

# PeopleDepot

PeopleDepot is a project of Hack for LA, a brigade of Code for America. PeopleDepot provides backend infrastructure to provide a single source of truth on people, program areas, and project data for all Hack for LA projects. PeopleDepot uses a Django database and Django REST Framework that acts as a repository of information for other infrastructure projects (e.g., VRMS, Hack for LA, Civic Tech Index, Tables). 

## Project context

The hardest part of running an all volunteer open source project organization is managing the flow of information to all the people and projects that need it.  It can end up taking more time than the projects themselves. This project seeks to create an infrastructure that will automate everything that can be automated and do away with manual storage of duplicate information across projects.

- Recruiting members (Website: Project info and meeting times)
- Onboarding members to resources (Tables:GitHub, Google Calendar, Google Drives, etc.)
- Helping members find roles (Civic Tech Jobs: roles and project info)
- Managing team permissions (VRMS: GitHub, Google Calendar, Google Drives, etc.)

## Technology used

- [Docker][docker-docs]
- [Django][django-docs]
- [DjangoRestFramework][drf-docs]
- [PostgreSQL][postgres-docs]

## How to contribute

1. Join our organization by going through [Hack for LA onboarding][HfLA onboarding]. It's free to join!
2. Read the [onboarding section of our WIKI](https://github.com/hackforla/peopledepot/wiki/Developer-Onboarding).
3. Read our [Contributing Guide][contributing] and follow the steps.

## Contact info

Contact us in the people-depot channel on Slack.

## Licensing

Include details about the project's open source status.

<!-- References section -->

[docker-docs]: https://www.postgresql.org/docs/
[django-docs]: https://docs.djangoproject.com/
[drf-docs]: https://www.django-rest-framework.org/tutorial/quickstart/
[postgres-docs]: https://www.postgresql.org/docs/
[contributing]: ./docs/contributing.md
[HfLA onboarding]: https://www.hackforla.org/getting-started
