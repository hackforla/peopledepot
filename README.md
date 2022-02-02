# Project title and description

Include a project description that explains **what** your project is and **why** it exists. Aim for no more than 3-5 concise sentences. For example, you might say:

{Project Name} is a project of Hack for LA. Hack for LA is a brigade of a Code for America that exists to {your mission}. {Project Name} helps {target users} accomplish {goal of project}. The {app/site/thing you're building}'s main features include {very brief feature descriptions}.

### Project context

Civic projects often exist within a larger context that may include multiple stakeholders, historic relationships, associated research, or other details that are relevant but not *required* for direct contributions. Gathering these details in one place is useful, but the ReadMe isn't that place. Use this section to [link to a Google Doc](#) or other documentation repository where contributors can dig in if they so choose. This is also a good place to link to your Code of Conduct.

### Technology used

- [Docker][docker-docs]
- [Django][django-docs]
- [DjangoRestFramework][drf-docs]
- [PostgreSQL][postgres-docs]

# How to contribute

Explain the different ways people can contribute. For example:

- Join the team {on Slack/at our weekly hack night/etc}.
- To help with user research, {do ABC}.
- To provide design support, {do XYZ}.
- To contribute to the code, follow the instructions below.

Remember to provide direct links to each channel.

## Installation instructions

---

**Note:** See [Contributing.md][contributing] for full instructions

---

1. Install or make sure [docker][docker-install] and [docker-compose][docker-compose-install] are installed on your computer

```
    docker -v
    docker-compose -v
```

2. Clone this repo and change to the project root directory

```
    git clone https://github.com/hackforla/peopledepot.git
    cd peopledepot
```

3. Create .env.dev from .env.dev-sample

```
    cp .env.dev-sample .env.dev
```

4. Build the image and run the containers

```
    docker-compose up --build
```

5. In another terminal, run migrations

```
    docker-compose exec web python manage.py migrate
```

6. Create a super user for logging into the web admin interface

```
    docker-compose exec web python manage.py createsuperuser
```

7. Browse to the web admin interface at `http://localhost:8000/admin/`

### Testing

1. Make sure containers are running

```
    docker-compose up -d
```

2. Run all tests

```
    docker-compose exec web pytest
```

### Working with issues

- Explain how to submit a bug.
- Explain how to submit a feature request.
- Explain how to contribute to an existing issue.

To create a new issue, please use the blank issue template (available when you click New Issue).  If you want to create an issue for other projects to use, please create the issue in your own repository and send a slack message to one of your hack night hosts with the link.

### Working with forks and branches

- Explain your guidelines here.

### Working with pull requests and reviews

- Explain your process.

# Contact info

Include at least one way (or more, if possible) to reach your team with questions or comments.

### Licensing

Include details about the project's open source status.

<!-- References section -->

[docker-docs]: https://www.postgresql.org/docs/
[django-docs]: https://docs.djangoproject.com/
[drf-docs]: https://www.django-rest-framework.org/tutorial/quickstart/
[postgres-docs]: https://www.postgresql.org/docs/
[contributing]: ./docs/contributing.md
[docker-install]: https://docs.docker.com/get-docker/
[docker-compose-install]: https://docs.docker.com/compose/install/
