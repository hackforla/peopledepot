from core.models import PermissionType
from core.models import Project
from core.models import User
from core.models import UserPermissions
from core.tests.utils.seed_constants import password
from core.tests.utils.utils_test import show_test_info


class SeedUser:
    users = {}

    def __init__(self, first_name, description):
        self.first_name = first_name
        self.last_name = description
        self.user_name = f"{first_name}@example.com"
        self.email = self.user_name
        self.user = SeedUser.create_user(first_name=first_name, description=description)
        self.users[first_name] = self.user

    @classmethod
    def get_user(cls, first_name):
        return cls.users.get(first_name)

    @classmethod
    def create_user(cls, *, first_name, description=None):
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
        cls.users[first_name] = user
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
