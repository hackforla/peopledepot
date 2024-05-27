from django.db import migrations

from core.models import PermissionType
from core.constants import PermissionValue


def run(__code__, __reverse_code__):
    items = [
        PermissionValue.project_admin,
        PermissionValue.practice_area_admin,
        PermissionValue.global_admin,
        PermissionValue.project_team_member,
        PermissionValue.practice_area_team_member,
        PermissionValue.verified_user,
    ]
    for name in items:
        PermissionType.objects.create(name=name)


class Migration(migrations.Migration):
    initial = True
    dependencies = [("data", "0003_sdg_seed")]

    operations = [migrations.RunPython(run, migrations.RunPython.noop)]
