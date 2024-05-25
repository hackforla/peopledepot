import copy
from core.models import Project, User
from core.tests.utils.seed_constants import (website_project, people_depot_project)
from core.constants import (project_lead, project_team_member, global_admin, verified_user)
from django.contrib.auth import get_user_model
from core.tests.utils.seed_user import SeedUser
UserModel = get_user_model()
from core.tests.utils.seed_data import Seed


class UserData2:   
    data_loaded = False
    @classmethod
    def load_data(cls):
        projects = [website_project, people_depot_project]
        for project_name in projects:
            project = Project.objects.create(name=project_name)
            project.save()
            
        Seed.wanda = SeedUser("Wanda", "Website project lead")
        Seed.wally = SeedUser("Wally", "Website member")
        Seed.winona = SeedUser("Winona", "Website member")
        Seed.zani   = SeedUser ("Zani", "Website member and People Depot project lead")
        Seed.patti = SeedUser("Patti", "People Depot member")
        Seed.patrick = SeedUser("Patrick", "People Depot project lead")
        Seed.garry = SeedUser("Garry", "Global admin")
        Seed.valerie = SeedUser("Valerie", "Verified user, no project")

        related_data = [
            {"first_name": Seed.wanda.first_name, "project_name": website_project, "permission_type_name": project_lead},
            {"first_name": Seed.wally.first_name, "project_name": website_project, "permission_type_name": project_team_member},
            {"first_name": Seed.winona.first_name, "project_name": website_project, "permission_type_name": project_team_member},
            {"first_name": Seed.zani.first_name, "project_name": people_depot_project, "permission_type_name": project_team_member},
            {"first_name": Seed.patti.first_name, "project_name": people_depot_project, "permission_type_name": project_team_member},
            {"first_name": Seed.patrick.first_name, "project_name": people_depot_project, "permission_type_name": project_lead},
            {"first_name": Seed.garry.first_name, "permission_type_name": global_admin},
            {"first_name": Seed.valerie.first_name, "permission_type_name": verified_user},
            {"first_name": Seed.zani.first_name, "project_name": website_project, "permission_type_name": project_lead},
        ]

        for data in related_data:
            user = SeedUser.get_user(data["first_name"])
            params = copy.deepcopy(data)
            del params["first_name"]
            SeedUser.create_related_data (user=user, **params)
        
        for user in User.objects.all():
            print("debug userx", user.first_name)        

    @classmethod
    def initialize_data(cls):
        if not cls.data_loaded:
            cls.load_data()
        else:
            print("Data already loaded")


