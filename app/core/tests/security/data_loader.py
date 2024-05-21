from core.models import User
from .constants import (website_project, people_depot_project, project_lead, project_team_member, global_admin, verified_user, wanda_name, wally_name, winona_name, zani_name, patti_name, patrick_name, paul_name, garry_name, valerie_name)

class UserData:   
    data_loaded = False
    users = {}
    wally_user = None
    wanda_user = None
    winona_user = None
    zani_user = None
    patti_user = None
    patrick_user = None
    paul_user = None

    @classmethod
    def get_user(cls, first_name):
        return cls.users.get(first_name)

    @classmethod
    def create_user(cls, *, first_name, project_name=None, permission_type_name, other_user_data={}):
        last_name = f"{permission_type_name}{project_name}"
        email = f"{first_name}{last_name}@example.com"
        username = email

        print("Creating user", first_name)
        user = User.objects.create(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email   
        )
        cls.users[first_name] = user

    @classmethod
    def load_data(cls):
        user_data = [
            {"first_name": wanda_name, "project_name": website_project, "permission_type_name": project_lead},
            {"first_name": wally_name, "project_name": website_project, "permission_type_name": project_team_member},
            {"first_name": winona_name, "project_name": website_project, "permission_type_name": project_team_member},
            {"first_name": zani_name, "project_name": people_depot_project, "permission_type_name": project_team_member},
            {"first_name": patti_name, "project_name": people_depot_project, "permission_type_name": project_team_member},
            {"first_name": patrick_name, "project_name": people_depot_project, "permission_type_name": project_lead},
            {"first_name": paul_name, "permission_type_name": global_admin},
            {"first_name": garry_name, "permission_type_name": verified_user},
            {"first_name": valerie_name, "permission_type_name": verified_user}
        ]
        for data in user_data:
            cls.create_user(**data)


    @classmethod
    def initialize_data(cls):
        print("BaseTestCase: setUpTestData")
        if not cls.data_loaded:
            cls.load_data()
            cls.data_loaded = True
            
        cls.wally_user = cls.get_user(wally_name)
        cls.wanda_user = cls.get_user(wanda_name)
        cls.winona_user = cls.get_user(winona_name)
        cls.zani_user = cls.get_user(zani_name)
        cls.patti_user = cls.get_user(patti_name)
        cls.patrick_user = cls.get_user(patrick_name)
        cls.paul_user = cls.get_user(paul_name)
        cls.garry_user = cls.get_user(garry_name)
        cls.valerie_user = cls.get_user(valerie_name)

# # data_loader.py

# class DataLoader:
#     user_data_loaded = False
#     wally_name = "Wally"
#     wanda_name = "Wanda"
#     winona_name = "Winona"
#     zani_name = "Zani"
#     patti_name = "Patti"
#     patrick_name = "Patrick"
#     paul_name = "Paul"
#     garry_name = "Garry"
#     valerie_name = "Valerie"
#     website_project = "website"
#     people_depot_project = "people-depot"
#     project_lead = "ProjectLead"
#     project_team_member = "ProjectMember"
#     global_admin = "GlobalAdmin"
#     verified_user = "VerifiedUser"

#     @classmethod
#     def prepopulate_test_data(cls):
#         if not cls.data_loaded:
#             print("Creating data")
#             cls.load_data()
#             cls.user_data_loaded = True

#     @staticmethod
#     def load_data():
#         from django.core.management import call_command

#         # Load your data here, e.g., calling a custom management command
#         call_command('your_custom_management_command_to_load_data')
