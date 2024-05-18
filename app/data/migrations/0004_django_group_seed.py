from django.db import migrations

from django.contrib.auth.models import Group
from data.group_data import PROJECT_LEAD, \
        PRACTICE_AREA_LEAD,\
        GLOBAL_ADMIN,\
        PROJECT_TEAM_MEMBER,\
        PRACTICE_AREA_TEAM_MEMBER,\
        VERIFIED_USER\


def run(__code__, __reverse_code__):
    items = [
        PROJECT_LEAD,
        PRACTICE_AREA_LEAD,
        GLOBAL_ADMIN,
        PROJECT_TEAM_MEMBER,
        PRACTICE_AREA_TEAM_MEMBER,
        VERIFIED_USER,
    ]
    for name in items:
        Group.objects.create(name=name)


class Migration(migrations.Migration):
    initial = True
    dependencies = [("data", "0003_sdg_seed")]

    operations = [migrations.RunPython(run, migrations.RunPython.noop)]
