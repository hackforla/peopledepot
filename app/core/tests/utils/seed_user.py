from dataclasses import dataclass
from typing import Dict
from typing import List

from core.models import PermissionType
from core.models import PracticeArea
from core.models import Project
from core.models import User
from core.models import UserPermission
from core.tests.utils.seed_constants import password


@dataclass
class UserRelatedData:
    first_name: str
    permission_type_name: str
    project_name: str = None
    practice_area_name: str = None


class UserRelatedData2:
    user: User
    related_data: list[UserRelatedData]

    def __init__(self, user: User, related_data: list[UserRelatedData]):
        self.user = user
        self.related_data = related_data


class SeedUser:
    """Summary
    Attributes:
        seed_users_list (dict): Populated by the create_user method.
        Used to store the users created by the SeedUser.create_user.
        Users are retrieved by first name.  The code uses constants
        when creating and getting seed users.
        _assocs (list): List of tuples containing (UserRelatedData, User) pairs
    """

    seed_users_list = {}
    seed_users_list2: dict[str, list[UserRelatedData2]] = {}
    _assocs = []

    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name
        self.user_name = f"{first_name}{last_name}@example.com"
        self.email = self.user_name
        self.user = SeedUser.create_user(first_name=first_name, description=last_name)
        self.seed_users_list[first_name] = self.user
        self.seed_users_list2[first_name] = UserRelatedData2(self.user, [])

    @classmethod
    def create_user2(cls, user_data: UserRelatedData):
        """Creates a user with the given first_name and description and
        stores the user in the seed_users_list dictionary.
        """
        user = cls.create_user(first_name=user_data.first_name)
        cls.create_related_data(
            user=user,
            permission_type_name=user_data.permission_type_name,
            project_name=user_data.project_name,
            practice_area_name=user_data.practice_area_name,
        )
        # Note: _assocs is populated in create_related_data
        return user

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
        cls.seed_users_list2[first_name] = UserRelatedData2(user, [])
        user.save()
        return user

    @classmethod
    def create_related_data(
        cls,
        *,
        user: User,
        permission_type_name: str,
        project_name: str = None,
        practice_area_name: str = None,
    ) -> UserPermission:
        """
        Create a UserPermission for the given user.

        Args:
            user (User): The user to assign permissions to.
            permission_type_name (str): Name of the PermissionType to assign.
            project_name (str, optional): Name of the Project to link the permission to.
                                          If None, permission is global.
            practice_area_name (str, optional): Name of the PracticeArea to link the permission to.

        Returns:
            UserPermission: The created UserPermission instance.
        """
        # Retrieve PermissionType object from DB
        permission_type = PermissionType.objects.get(name=permission_type_name)
        project_data = (
            {"project": Project.objects.get(name=project_name)} if project_name else {}
        )
        practice_area_data = (
            {"practice_area": PracticeArea.objects.get(name=practice_area_name)}
            if practice_area_name
            else {}
        )
        user_permission = UserPermission.objects.create(
            user=user,
            permission_type=permission_type,
            **project_data,
            **practice_area_data,
        )
        user_permission.save()

        # Store UserRelatedData with the user
        user_related = UserRelatedData(
            first_name=user.first_name,
            permission_type_name=permission_type_name,
            project_name=project_name,
            practice_area_name=practice_area_name,
        )
        seed_user2 = cls.seed_users_list2.get(user.first_name)
        if seed_user2 is None:
            raise ValueError(f"User {user.first_name} not found in seed_users_list")
        seed_user2.related_data.append(user_related)

        cls._assocs.append((user_related, user))

        return user_permission

    @classmethod
    def get_user(cls, first_name):
        """Looks up user info from seed_users_list dictionary.
        For more info, see notes on seed_users_list in the class docstring.
        """
        return cls.seed_users_list.get(first_name)

    @classmethod
    def get_user2(cls, assoc_lookup):
        """Looks up user info from seed_users_list dictionary.
        For more info, see notes on seed_users_list in the class docstring.
        """
        for assoc in cls._assocs:
            if assoc[0] == assoc_lookup:
                return assoc[1]
        raise ValueError(f"No user found with permission type {assoc_lookup}")

    @classmethod
    def get_user_by_related_data(
        cls,
        permission_type_name: str,
        project_name: str = None,
        practice_area_name: str = None,
    ) -> User:
        """Looks up user info from seed_users_list dictionary.
        For more info, see notes on seed_users_list in the class docstring.
        """
        lookup = [permission_type_name]
        if project_name:
            lookup.append(project_name)
        if practice_area_name:
            lookup.append(practice_area_name)
        for assoc in cls._assocs:
            if assoc[0] == lookup:
                return assoc[1]
        raise ValueError(f"No user found with permission type {lookup}")

    @classmethod
    def get_user3(
        cls,
        permission_type_name: str,
        project_name: str = None,
        practice_area_name: str = None,
    ) -> User:
        """
        Looks up user based on UserRelatedData stored in _assocs.

        Args:
            permission_type_name (str): The permission type name to match
            project_name (str, optional): The project name to match
            practice_area_name (str, optional): The practice area name to match

        Returns:
            User: The user associated with the matching UserRelatedData

        Raises:
            ValueError: If no matching user is found
        """
        for user_data, user in cls._assocs:
            if (
                user_data.permission_type_name == permission_type_name
                and user_data.project_name == project_name
                and user_data.practice_area_name == practice_area_name
            ):
                return user

        raise ValueError(
            f"No user found with permission_type={permission_type_name}, "
            f"project={project_name}, practice_area={practice_area_name}"
        )
