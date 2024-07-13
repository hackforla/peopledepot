import copy

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

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

UserModel = get_user_model()


class LoadData:
    data_loaded = False

    @classmethod
    def load_data(cls):
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
        SeedUser.create_user(
            first_name="Patrick", description="People Depot project lead"
        )
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

    @classmethod
    def initialize_data(cls):
        if not cls.data_loaded:
            cls.load_data()
        else:
            print("Data already loaded")


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        LoadData.initialize_data()
        self.stdout.write(self.style.SUCCESS("Data initialized successfully"))
