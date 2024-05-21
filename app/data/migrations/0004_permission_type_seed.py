from django.db import migrations

from core.models import PermissionType
from core.constants import project_lead, \
        practice_area_lead,\
        global_admin,\
        project_team_member,\
        practice_area_team_member,\
        verified_user\


def run(__code__, __reverse_code__):
    items = [
        project_lead,
        practice_area_lead,
        global_admin,
        project_team_member,
        practice_area_team_member,
        verified_user,
    ]
    for name in items:
        PermissionType.objects.create(name=name)


class Migration(migrations.Migration):
    initial = True
    dependencies = [("data", "0003_sdg_seed")]

    operations = [migrations.RunPython(run, migrations.RunPython.noop)]
