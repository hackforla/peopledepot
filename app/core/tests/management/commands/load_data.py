import copy

from constants import project_lead
from constants import project_member
from core.models import Project
from core.tests.utils.seed_constants import garry_name
from core.tests.utils.seed_constants import patrick_project_lead
from core.tests.utils.seed_constants import patti_name
from core.tests.utils.seed_constants import people_depot_project
from core.tests.utils.seed_constants import valerie_name
from core.tests.utils.seed_constants import wally_name
from core.tests.utils.seed_constants import wanda_project_lead
from core.tests.utils.seed_constants import website_project_name
from core.tests.utils.seed_constants import winona_name
from core.tests.utils.seed_constants import zani_name
from core.tests.utils.seed_user import SeedUser


def load_data():
    """Populalates projects, users, and userpermissions with seed data
    used by the tests in the core app.

    Called from django_db_setup which is automatcallly called by pytest-django
    before any test is executed.

    Creates website_project and people_depot projects.  Populates users
    as follows:
    - Wanda is the project lead for the website project
    - Wally and Winona are members of the website project
    - Patti is a member of the People Depot project
    - Patrick is the project lead for the People Depot project

    - Garry is a global admin
    - Zani is a member of the website project and the project lead for the People Depot project
    - Valerie is a verified user with no UserPermissions assignments.
    """
    projects = [website_project_name, people_depot_project]
    for project_name in projects:
        project = Project.objects.create(name=project_name)
        project.save()
    SeedUser.create_user(first_name="Wanda", description="Website project lead")
    SeedUser.create_user(first_name="Wally", description="Website member")
    SeedUser.create_user(first_name="Winona", description="Website member")
    SeedUser.create_user(
        first_name="Zani",
        description="Website member and People Depot project lead",
    )
    SeedUser.create_user(first_name="Patti", description="People Depot member")
    SeedUser.create_user(first_name="Patrick", description="People Depot project lead")
    SeedUser.create_user(first_name="Garry", description="Global admin")
    SeedUser.get_user(garry_name).is_superuser = True
    SeedUser.get_user(garry_name).save()
    SeedUser.create_user(first_name=valerie_name, description="Verified user")

    related_data = [
        {
            "first_name": wanda_project_lead,
            "project_name": website_project_name,
            "permission_type_name": project_lead,
        },
        {
            "first_name": wally_name,
            "project_name": website_project_name,
            "permission_type_name": project_member,
        },
        {
            "first_name": winona_name,
            "project_name": website_project_name,
            "permission_type_name": project_member,
        },
        {
            "first_name": patti_name,
            "project_name": people_depot_project,
            "permission_type_name": project_member,
        },
        {
            "first_name": patrick_project_lead,
            "project_name": people_depot_project,
            "permission_type_name": project_lead,
        },
        {
            "first_name": zani_name,
            "project_name": people_depot_project,
            "permission_type_name": project_lead,
        },
        {
            "first_name": zani_name,
            "project_name": website_project_name,
            "permission_type_name": project_member,
        },
    ]

    for data in related_data:
        user = SeedUser.get_user(data["first_name"])
        params = copy.deepcopy(data)
        del params["first_name"]
        SeedUser.create_related_data(user=user, **params)
