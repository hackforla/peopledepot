import copy

from constants import GLOBAL_ADMIN
from constants import ADMIN_PROJECT
from constants import MEMBER_PROJECT
from constants import PRACTICE_LEAD_PROJECT
from core.models import Project

from .seed_constants import garry_name
from .seed_constants import patrick_practice_lead
from .seed_constants import patti_name
from .seed_constants import people_depot_project
from .seed_constants import valerie_name
from .seed_constants import wally_name
from .seed_constants import wanda_admin_project
from .seed_constants import website_project_name
from .seed_constants import winona_name
from .seed_constants import zani_name
from .seed_user import SeedUser


def seed_user_test_data():
    """Populalates projects, users, and userpermissions with seed data
    that is used by the tests in the core app.

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
    - Valerie is a verified user with no UserPermission assignments.
    """
    projects = [website_project_name, people_depot_project]
    for project_name in projects:
        project = Project.objects.create(name=project_name)
        project.save()
    SeedUser.create_user(
        first_name=wanda_admin_project, description="Website project admin"
    )
    SeedUser.create_user(first_name=wally_name, description="Website member")
    SeedUser.create_user(first_name=winona_name, description="Website member")
    SeedUser.create_user(
        first_name=zani_name,
        description="Website member and People Depot project admin",
    )
    SeedUser.create_user(first_name=patti_name, description="People Depot member")
    SeedUser.create_user(
        first_name=patrick_practice_lead, description="People Depot project admin"
    )
    SeedUser.create_user(first_name=garry_name, description="Global admin")
    SeedUser.get_user(garry_name).save()
    SeedUser.create_user(first_name=valerie_name, description="Verified user")

    related_data = [
        {"first_name": garry_name, "permission_type_name": GLOBAL_ADMIN},
        {
            "first_name": garry_name,
            "project_name": website_project_name,
            "permission_type_name": ADMIN_PROJECT,
        },
        {
            "first_name": wanda_admin_project,
            "project_name": website_project_name,
            "permission_type_name": ADMIN_PROJECT,
        },
        {
            "first_name": wally_name,
            "project_name": website_project_name,
            "permission_type_name": MEMBER_PROJECT,
        },
        {
            "first_name": winona_name,
            "project_name": website_project_name,
            "permission_type_name": MEMBER_PROJECT,
        },
        {
            "first_name": patti_name,
            "project_name": people_depot_project,
            "permission_type_name": MEMBER_PROJECT,
        },
        {
            "first_name": patrick_practice_lead,
            "project_name": people_depot_project,
            "permission_type_name": PRACTICE_LEAD_PROJECT,
        },
        {
            "first_name": zani_name,
            "project_name": people_depot_project,
            "permission_type_name": ADMIN_PROJECT,
        },
        {
            "first_name": zani_name,
            "project_name": website_project_name,
            "permission_type_name": MEMBER_PROJECT,
        },
    ]

    for data in related_data:
        user = SeedUser.get_user(data["first_name"])
        params = copy.deepcopy(data)
        del params["first_name"]
        SeedUser.create_related_data(user=user, **params)
