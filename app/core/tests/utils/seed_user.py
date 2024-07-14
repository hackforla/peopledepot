from core.models import PermissionType
from core.models import Project
from core.models import User
from core.models import UserPermissions
from core.tests.utils.seed_constants import password
from core.tests.utils.utils_test import show_test_info


class SeedUser:
    """Summary
    Attributes:
        seed_users_list (dict): Populated by the create_user method.
        Used to store the users created by the SeedUser.create_user.
        This is called indirectly by django_db_setup in conftest.py.
        django_db_setup calls load_data which executes the create_user
        and create_related_data methods in this class.
    """

    seed_users_list = {}

    def __init__(self, first_name, description):
        self.first_name = first_name
        self.last_name = description
        self.user_name = f"{first_name}@example.com"
        self.email = self.user_name
        self.user = SeedUser.create_user(first_name=first_name, description=description)
        self.seed_users_list[first_name] = self.user

    @classmethod
    def get_user(cls, first_name):
        """Looks up user info from seed_users_list dictionary.
        For more info, see notes on seed_users_list in the class docstring.
        """
        return cls.seed_users_list.get(first_name)

    @classmethod
    def create_user(cls, *, first_name, description=None):
        """Creates a user with the given first_name and description and
        stores the user in the seed_users_list dictionary.
        """
        last_name = f"{description}"
        email = f"{first_name}{last_name}@example.com"
        username = first_name

        user = User.objects.create(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            is_active=True,
        )
        user.set_password(password)
        cls.seed_users_list[first_name] = user
        user.save()
        return user

    @classmethod
    def create_related_data(
        cls, *, user=None, permission_type_name=None, project_name=None
    ):
        permission_type = PermissionType.objects.get(name=permission_type_name)
        if project_name:
            project_data = {"project": Project.objects.get(name=project_name)}
        else:
            project_data = {}
        user_permission = UserPermissions.objects.create(
            user=user, permission_type=permission_type, **project_data
        )
        show_test_info(
            "Created user permission " + user.username + " " + permission_type.name
        )
        user_permission.save()
        return user_permission
