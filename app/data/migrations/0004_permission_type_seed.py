from django.db import migrations

from constants import practice_area_admin, project_lead, project_team_member
from core.models import PermissionType, Sdg


def forward(__code__, __reverse_code__):
    PermissionType.objects.create(name=project_lead, description="Project Lead")
    PermissionType.objects.create(
        name=practice_area_admin, description="Practice Area Admin"
    )
    PermissionType.objects.create(
        name=practice_area_admin, description="Practice Area Admin"
    )
    PermissionType.objects.create(
        name=project_team_member, description="Project Team Member"
    )


def reverse(__code__, __reverse_code__):
    PermissionType.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [("data", "0003_sdg_seed")]

    operations = [migrations.RunPython(forward, reverse)]
