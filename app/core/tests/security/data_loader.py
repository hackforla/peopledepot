import copy
from core.models import PermissionAssignment, PermissionType, Project, User
from .seed_constants import (website_project, people_depot_project, wanda_name, wally_name, winona_name, zani_name, patti_name, patrick_name, paul_name, garry_name, valerie_name)
from core.constants import (project_lead, project_team_member, global_admin, verified_user)

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
        return user
        
    def create_related_data(*, user=None, permission_type_name=None, project_name=None):
        permission_type = PermissionType.objects.get(name=permission_type_name)
        if project_name:
            project_data = { "project":  Project.objects.get(name=project_name)}
        else:
            project_data = {}
        user_permission = PermissionAssignment.objects.create(user=user, permission_type=permission_type, **project_data)
        print("Created user permission", user_permission)
        user_permission.save()
        return user_permission
    
    @classmethod
    def load_data(cls):
        projects = [website_project, people_depot_project]
        for project_name in projects:
            project = Project.objects.create(name=project_name)
            project.save()
            
        user_names = [wanda_name, wally_name, winona_name, zani_name, patti_name, patrick_name, paul_name, garry_name, valerie_name]
        for name in user_names:
            cls.create_user(first_name=name, permission_type_name=verified_user)
            
        related_data = [
            {"first_name": wanda_name, "project_name": website_project, "permission_type_name": project_lead},
            {"first_name": wally_name, "project_name": website_project, "permission_type_name": project_team_member},
            {"first_name": winona_name, "project_name": website_project, "permission_type_name": project_team_member},
            {"first_name": zani_name, "project_name": people_depot_project, "permission_type_name": project_team_member},
            {"first_name": patti_name, "project_name": people_depot_project, "permission_type_name": project_team_member},
            {"first_name": patrick_name, "project_name": people_depot_project, "permission_type_name": project_lead},
            {"first_name": paul_name, "project_name": people_depot_project, "permission_type_name": project_team_member},
            {"first_name": garry_name, "permission_type_name": global_admin},
            {"first_name": valerie_name, "permission_type_name": verified_user},
            {"first_name": zani_name, "project_name": website_project, "permission_type_name": project_team_member},
        ]

        for data in related_data:
            user = cls.get_user(data["first_name"])
            params = copy.deepcopy(data)
            del params["first_name"]
            cls.create_related_data (user=user, permission_type_name=data["permission_type_name"], project_name=project_name)
        

    @classmethod
    def initialize_data(cls):
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

