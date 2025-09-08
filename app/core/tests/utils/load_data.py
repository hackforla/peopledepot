import copy

from constants import admin_global, admin_project, member_project, practice_lead_project
from core.models import Project
from core.tests.utils.seed_constants import (
    garry_name, patrick_practice_lead, patti_name, people_depot_project,
    valerie_name, wally_name, wanda_admin_project, website_project_name,
    winona_name, zani_name
)
from core.tests.utils.seed_user import SeedUser


def load_data():
    """
    Populates projects, users, and user permissions with seed data
    used by tests in the core app.

    Called automatically by pytest-django via `django_db_setup`.

    Creates two projects:
        - Website Project
        - People Depot Project

    Populates users with specific roles and project memberships:
        - Wanda: project lead for Website project
        - Wally, Winona: members of Website project
        - Patti: member of People Depot project
        - Patrick: project lead for People Depot project
        - Garry: global admin
        - Zani: member of Website project and project lead for People Depot project
        - Valerie: verified user with no permissions

    The user and permission setup allows tests to verify:
        - Global vs. project-level permissions
        - Team membership filtering
        - Access control for non-permissioned users
    """
    # Step 1: Create projects
    projects = [website_project_name, people_depot_project]
    for project_name in projects:
        project = Project.objects.create(name=project_name)
        project.save()  # Ensure project is persisted to DB

    # Step 2: Create users
    # Each user has a description for clarity in debugging and test logs
    SeedUser.create_user(first_name=wanda_admin_project, description="Website project admin")
    SeedUser.create_user(first_name=wally_name, description="Website member")
    SeedUser.create_user(first_name=winona_name, description="Website member")
    SeedUser.create_user(
        first_name=zani_name,
        description="Website member and People Depot project admin"
    )
    SeedUser.create_user(first_name=patti_name, description="People Depot member")
    SeedUser.create_user(first_name=patrick_practice_lead, description="People Depot project admin")
    SeedUser.create_user(first_name=garry_name, description="Global admin")
    SeedUser.get_user(garry_name).save()  # Save explicitly to trigger any signals or defaults
    SeedUser.create_user(first_name=valerie_name, description="Verified user")

    # Step 3: Define related user permissions
    # Each dictionary maps a user to a permission type, optionally scoped to a project
    related_data = [
        # Garry is global admin: can access everything in all tests
        {"first_name": garry_name, "permission_type_name": admin_global},
        # Garry as admin for Website project: allows project-specific tests
        {"first_name": garry_name, "project_name": website_project_name, "permission_type_name": admin_project},
        # Wanda: admin for Website project to test project admin permissions
        {"first_name": wanda_admin_project, "project_name": website_project_name, "permission_type_name": admin_project},
        # Wally and Winona: members of Website project to test team-level permissions
        {"first_name": wally_name, "project_name": website_project_name, "permission_type_name": member_project},
        {"first_name": winona_name, "project_name": website_project_name, "permission_type_name": member_project},
        # Patti: member of People Depot project to test isolated project membership
        {"first_name": patti_name, "project_name": people_depot_project, "permission_type_name": member_project},
        # Patrick: project lead for People Depot to test project lead permissions
        {"first_name": patrick_practice_lead, "project_name": people_depot_project, "permission_type_name": practice_lead_project},
        # Zani: admin for People Depot and member for Website to test multi-project scenarios
        {"first_name": zani_name, "project_name": people_depot_project, "permission_type_name": admin_project},
        {"first_name": zani_name, "project_name": website_project_name, "permission_type_name": member_project},
    ]

    # Step 4: Apply related permissions for each user
    for data in related_data:
        user = SeedUser.get_user(data["first_name"])
        # Copy data and remove first_name for create_related_data
        params = copy.deepcopy(data)
        del params["first_name"]
        # Create the user-project-permission relationship
        SeedUser.create_related_data(user=user, **params)
