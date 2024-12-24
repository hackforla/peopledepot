from django.db import migrations
from django.contrib.auth.models import Group

def create_group_permission(group_name, permission_name):
    from django.contrib.contenttypes.models import ContentType
    from django.contrib.auth.models import Permission

    # Create a placeholder content type
    placeholder_content_type, _ = ContentType.objects.get_or_create(
        app_label='global',
        model='globalpermission'
    )

    group, __created__ = Group.objects.get_or_create(name=group_name)
    permission, __created__ = Permission.objects.get_or_create(codename=permission_name, name=permission_name, content_type=placeholder_content_type)

    group.permissions.add(permission)

def create_group_and_permission(__app__, __schema_editor__):
    # Example group and permission names
    create_group_permission("kb_user", "get_api_user_app_kb")

class Migration(migrations.Migration):
    dependencies = [("data", "0008_userstatustype_seed")]

    operations = [
        migrations.RunPython(create_group_and_permission),
    ]
