import copy

from constants import ADMIN_GLOBAL
from constants import ADMIN_PROJECT
from constants import MEMBER_PROJECT
from constants import PRACTICE_LEAD_PROJECT
from core.models import Project
from core.tests.utils.seed_constants import garry_name
from core.tests.utils.seed_constants import patrick_practice_lead
from core.tests.utils.seed_constants import patti_name
from core.tests.utils.seed_constants import PROJECT2_NAME
from core.tests.utils.seed_constants import valerie_name
from core.tests.utils.seed_constants import wally_name
from core.tests.utils.seed_constants import wanda_admin_project
from core.tests.utils.seed_constants import PROJECT1_NAME
from core.tests.utils.seed_constants import winona_name
from core.tests.utils.seed_constants import zani_name
from core.tests.utils.seed_user import SeedUser
from core.tests.utils.seed_user import UserRelatedData


def load_data():
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
    projects = [PROJECT1_NAME, PROJECT2_NAME]
    for project_name in projects:
        project = Project.objects.create(name=project_name)
        project.save()

    # Create user with global admin and also project admin for project1
    global_admin_related_data = UserRelatedData (
        first_name=garry_name,
        permission_type_name=ADMIN_GLOBAL
    )
    adminUser = SeedUser.create_user2(global_admin_related_data)
    SeedUser.create_related_data(user=adminUser, permission_type_name=ADMIN_PROJECT, project_name=PROJECT1_NAME)

    # Create user with no permission types
    SeedUser.create_user(first_name=valerie_name, description="Verified user")      

    # Create user with project admin for project2 and also member for project1
    zani_related_data = UserRelatedData(
            first_name=zani_name,
            project_name=PROJECT2_NAME,
            permission_type_name=ADMIN_PROJECT,
        )
    zaniUser = SeedUser.create_user2(zani_related_data)
    SeedUser.create_related_data(
        user=zaniUser,
        permission_type_name=MEMBER_PROJECT,
        project_name=PROJECT1_NAME,
    )

    # Create other users with single permission type assignments
    related_data2 = [
        # User with project admin for project1
        UserRelatedData(
            first_name=wanda_admin_project,
            project_name=PROJECT1_NAME,
            permission_type_name=ADMIN_PROJECT,
        ),
        # User with project member for project1
        UserRelatedData(
            first_name=wally_name,
            project_name=PROJECT1_NAME,
            permission_type_name=MEMBER_PROJECT,
        ),
        # User with project member for project1
        UserRelatedData(
            first_name=winona_name,
            project_name=PROJECT1_NAME,
            permission_type_name=MEMBER_PROJECT,
        ),
        # User with project member for project2
        UserRelatedData(
            first_name=patti_name,
            project_name=PROJECT2_NAME,
            permission_type_name=MEMBER_PROJECT,
        ),
        # User with practice lead for project2
        UserRelatedData(
            first_name=patrick_practice_lead,
            project_name=PROJECT2_NAME,
            permission_type_name=PRACTICE_LEAD_PROJECT,
        ),
    ]

    for data in related_data2:
        SeedUser.create_user2(data)
