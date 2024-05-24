from app.core.models import PermissionAssignment, PermissionType, Project, User


class seed_user:    

    
    def __init__(self, first_name, last_name, description):
        self.first_name = first_name
        self.last_name = last_name
        self.user_name = f"{first_name}{description}"
        self.user = seed_user.create_user(first_name=first_name)
    
    
    @classmethod
    def get_user(cls, first_name):
        return cls.users.get(first_name)

    @classmethod
    def create_user(cls, *, first_name, project_name=None, other_user_data={}):
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
        user.save()
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
        