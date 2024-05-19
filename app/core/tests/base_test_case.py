from django.test import TestCase
from core.models import PermissionAssignment, PermissionType, Project, User
from data.group_data import PROJECT_LEAD, \
        GLOBAL_ADMIN,\
        PROJECT_TEAM_MEMBER,\
        VERIFIED_USER

WEBSITE_PROJECT = "website"
PEOPLE_DEPOT_PROJECT = "people-depot"

WANDA_USER_DATA = { "first_name": "Wanda", "project_name": WEBSITE_PROJECT,"permission_type_name": PROJECT_LEAD}
WALLY_USER_DATA = { "first_name": "Wally",  "project_name": WEBSITE_PROJECT,"permission_type_name": PROJECT_TEAM_MEMBER}
WINONA_USER_DATA = { "first_name": "Winona",  "project_name": WEBSITE_PROJECT,"permission_type_name": PROJECT_TEAM_MEMBER}
PATRICK_USER_DATA = { "first_name": "Patrick",  "project_name": PEOPLE_DEPOT_PROJECT,"permission_type_name": PROJECT_LEAD}
PATTI_USER_DATA = { "first_name": "Patti",  "project_name": PEOPLE_DEPOT_PROJECT,"permission_type_name": PROJECT_TEAM_MEMBER}
PERRY_USER_DATA = { "first_name": "Perry",  "project_name": PEOPLE_DEPOT_PROJECT,"permission_type_name": PROJECT_TEAM_MEMBER}
GARRY_USER_DATA = { "first_name": "Garry",  "permission_type_name": GLOBAL_ADMIN}
VALERIE_USER_DATA = { "first_name": "Valerie",  "permission_type_name": VERIFIED_USER}

ZANI_PEOPLE_DEPOT_DATA = { "first_name": "Zani",  "project_name": PEOPLE_DEPOT_PROJECT,"permission_type_name":PROJECT_LEAD}
ZANI_WEBSITE_ROLE_ASSIGNMENT_DATA = { "project_name": WEBSITE_PROJECT,"permission_type_name":PROJECT_TEAM_MEMBER}

def create_permission(*, user=None, permission_type_name=None, project_name=None):
    permission_type = PermissionType.objects.get(name=permission_type_name)
    if project_name:
        project_data = { "project":  Project.objects.get(name=project_name or "")}
    else:
        project_data = {}
    print("project_data", project_data)
    user_permission = PermissionAssignment.objects.create(user=user, permission_type=permission_type, **project_data)
    print("user_permission", user_permission)
    user_permission.save()
    return user_permission

def uppercase_to_camel_case(string):
    words = string.lower().split()
    camel_case_string = words[0] + ''.join(word.capitalize() for word in words[1:])
    return camel_case_string

def create_user_for_test(*, first_name=None, project_name=None, permission_type_name=None, other_user_data={}):
    permission_type_name_without_underscore = uppercase_to_camel_case(permission_type_name.replace("_", ""))
    first_name = first_name
    last_name = permission_type_name_without_underscore
    email = f"{first_name}{permission_type_name_without_underscore}".lower()+"@example.com"
    username = email
    
    user_basic = {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "username": username
    }
    user_data = {**user_basic, **other_user_data}

    user = User.objects.create(**user_data)

    create_permission(user=user, permission_type_name=permission_type_name, project_name=project_name)

      
    print("User created:", user)
    user.save()
    return user

class BaseTestCase(TestCase):
    WANDA_USER = None
    WALLY_USER = None
    WINONA_USER = None
    ZANI_USER = None
    PATRICK_USER = None
    PATTI_USER = None
    GARRY_USER = None
    VALERIE_USER = None

    @classmethod
    def setUpTestData(cls):
        Project.objects.create(name=WEBSITE_PROJECT)
        Project.objects.create(name=PEOPLE_DEPOT_PROJECT)
        cls.WANDA_USER = create_user_for_test(**WANDA_USER_DATA)
        cls.WALLY_USER = create_user_for_test(**WALLY_USER_DATA)
        cls.WINONA_USER = create_user_for_test(**WINONA_USER_DATA)

        cls.PATRICK_USER = create_user_for_test(**PATRICK_USER_DATA)
        cls.PATTI_USER = create_user_for_test(**PATTI_USER_DATA)
        cls.PERRY_USER = create_user_for_test(**PERRY_USER_DATA)

        cls.GARRY_USER = create_user_for_test(**GARRY_USER_DATA)
        cls.VALERIE_USER = create_user_for_test(**VALERIE_USER_DATA)
        
        cls.ZANI_USER = create_user_for_test(**ZANI_PEOPLE_DEPOT_DATA)
        create_permission( user = cls.ZANI_USER, **ZANI_WEBSITE_ROLE_ASSIGNMENT_DATA)
        print(PermissionAssignment.objects.all())
        
        

