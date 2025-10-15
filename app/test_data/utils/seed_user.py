from core.models import PermissionType
from core.models import Project
from core.models import User
from core.models import UserPermission

from .seed_constants import password


class SeedUser:
    """Summary
    Attributes:
        seed_users_list (dict): Populated by the create_user method.
        Used to store the users created by the SeedUser.create_user.
        Users are retrieved by first name.  The code uses constants
        when creating and getting seed users.
    """

    seed_users_list = {}

    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name
        self.user_name = f"{first_name}{last_name}@example.com"
        self.email = self.user_name
        self.user = SeedUser.create_user(first_name=first_name, description=last_name)
        self.seed_users_list[first_name] = self.user

    @classmethod
    def create_user(cls, *, first_name, description=None):
        """Creates a user with the given first_name and description and
        stores the user in the seed_users_list dictionary.
        """
        last_name = f"{description}"
        email = f"{first_name}@example.com"
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
        cls, *, user: User, permission_type_name: str, project_name: str = None
    ) -> UserPermission:
        """
        Create a UserPermission for the given user.

        Args:
            user (User): The user to assign permissions to.
            permission_type_name (str): Name of the PermissionType to assign.
            project_name (str, optional): Name of the Project to link the permission to.
                                          If None, permission is global.

        Returns:
            UserPermission: The created UserPermission instance.
        """
        # Retrieve PermissionType object from DB
        permission_type = PermissionType.objects.get(name=permission_type_name)
        if project_name:
            project_data = {"project": Project.objects.get(name=project_name)}
        else:
            project_data = {}
        user_permission = UserPermission.objects.create(
            user=user, permission_type=permission_type, **project_data
        )
        user_permission.save()
        return user_permission

    @classmethod
    def get_user(cls, first_name):
        """Looks up user info from seed_users_list dictionary.
        For more info, see notes on seed_users_list in the class docstring.
        """
        return cls.seed_users_list.get(first_name)
