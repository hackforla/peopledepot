from core.models import PermissionType
from core.models import Project
from core.models import User
from core.models import UserPermission
from core.tests.utils.seed_constants import password


class SeedUser:
    """
    Helper class to create and manage seed users for tests.

    Attributes:
        seed_users_list (dict): Stores users created via `create_user`.
            Keys are first names, values are User instances. Used for retrieval in tests.

    Methods:
        create_user: Create a new user with first name and optional description.
        create_related_data: Create UserPermission for a user, optionally linked to a project.
        get_user: Retrieve a previously created user by first name.
    """

    # Class-level dictionary storing all seed users for easy retrieval
    seed_users_list = {}

    def __init__(self, first_name: str, last_name: str):
        """
        Initialize a seed user and store it in `seed_users_list`.

        Args:
            first_name (str): User's first name; also used as key in seed_users_list.
            last_name (str): Description or last name for the user.
        """
        self.first_name = first_name
        self.last_name = last_name
        self.user_name = f"{first_name}{last_name}@example.com"
        self.email = self.user_name

        # Create the actual User instance and store in the class dictionary
        self.user = SeedUser.create_user(first_name=first_name, description=last_name)
        self.seed_users_list[first_name] = self.user

    @classmethod
    def create_user(cls, *, first_name: str, description: str = None) -> User:
        """
        Create a user instance and save it in the database and seed_users_list.

        Args:
            first_name (str): The user's first name (used as username and key).
            description (str, optional): Stored in last_name field for clarity.

        Returns:
            User: The created Django User instance.
        """
        last_name = f"{description}" if description else ""
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

        # Optionally link the permission to a project
        project_data = (
            {"project": Project.objects.get(name=project_name)} if project_name else {}
        )

        user_permission = UserPermission.objects.create(
            user=user, permission_type=permission_type, **project_data
        )
        user_permission.save()
        return user_permission

    @classmethod
    def get_user(cls, first_name: str) -> User | None:
        """
        Retrieve a previously created user from seed_users_list.

        Args:
            first_name (str): First name of the user to retrieve.

        Returns:
            User or None: The User instance if found, else None.
        """
        return cls.seed_users_list.get(first_name)
