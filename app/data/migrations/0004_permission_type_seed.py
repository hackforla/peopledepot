from django.db import migrations

from constants import practice_area_admin, project_lead, project_member
from core.models import PermissionType, Sdg


def forward(__code__, __reverse_code__):
    PermissionType.objects.create(name=project_lead, description="Project Lead", rank=1)
    PermissionType.objects.create(
        name=practice_area_admin, description="Practice Area Admin", rank=2
    )
    PermissionType.objects.create(
        name=project_member, description="Project Team Member", rank=3
    )


def reverse(__code__, __reverse_code__):
    PermissionType.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ("data", "0003_sdg_seed"),
        ("core", "0025_permissiontype_rank_and_more"),
    ]

    operations = [migrations.RunPython(forward, reverse)]
