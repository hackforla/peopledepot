from django.test import TestCase
from core.models import User
from data.group_data import PROJECT_LEAD, \
        GLOBAL_ADMIN,\
        PROJECT_TEAM_MEMBER,\
        VERIFIED_USER

WEBSITE_PROJECT = "website"
PEOPLE_DEPOT_PROJECT = "people-depot"

WANDA_USER_DATA = { "name": "Wanda", "project": WEBSITE_PROJECT, "group":PROJECT_LEAD}
WALLY_USER_DATA = { "name": "Wally",  "project": WEBSITE_PROJECT, "group":PROJECT_TEAM_MEMBER}
WINONA_USER_DATA = { "name": "Winona",  "project": WEBSITE_PROJECT, "group":PROJECT_TEAM_MEMBER}
ZANI_PEOPLE_DEPOT_DATA = { "name": "Zani",  "project": PEOPLE_DEPOT_PROJECT, "group":PROJECT_LEAD}
PATRICK_USER_DATA = { "name": "Patrick",  "project": PEOPLE_DEPOT_PROJECT, "group":PROJECT_LEAD}
PATTI_USER_DATA = { "name": "Patti",  "project": PEOPLE_DEPOT_PROJECT, "group":PROJECT_TEAM_MEMBER}
GARRY_USER_DATA = { "name": "Garry",  "group": GLOBAL_ADMIN}
VALERIE_USER_DATA = { "name": "Valerie",  "group": VERIFIED_USER}

def uppercase_to_camel_case(string):
    words = string.lower().split()
    camel_case_string = words[0] + ''.join(word.capitalize() for word in words[1:])
    return camel_case_string

def create_user_for_test(user_data):
    group = user_data.get("group")
    group_without_underscore = uppercase_to_camel_case(group.replace("_", ""))
    first_name = user_data["name"]
    last_name = group_without_underscore
    email = f"{first_name}{group_without_underscore}".lower()+"@example.com"
    username = email
    
    user = User.objects.create(
        first_name=first_name,
        last_name=last_name,
        email=email,
        username=username        
    )
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
        cls.WANDA_USER = create_user_for_test(WANDA_USER_DATA)
        cls.WALLY_USER = create_user_for_test(WALLY_USER_DATA)
        cls.WINONA_USER = create_user_for_test(WINONA_USER_DATA)
        cls.ZANI_USER = create_user_for_test(ZANI_PEOPLE_DEPOT_DATA)
        cls.PATRICK_USER = create_user_for_test(PATRICK_USER_DATA)
        cls.PATTI_USER = create_user_for_test(PATTI_USER_DATA)
        cls.GARRY_USER = create_user_for_test(GARRY_USER_DATA)
        cls.VALERIE_USER = create_user_for_test(VALERIE_USER_DATA)
