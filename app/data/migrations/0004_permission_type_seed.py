from django.db import migrations

from constants import practice_lead_project, admin_project, member_project
from core.models import PermissionType, Sdg


def forward(__code__, __reverse_code__):
    PermissionType.objects.create(
        name=admin_project, description="Project admin", rank=1
    )
    PermissionType.objects.create(
        name=practice_lead_project,
        description="Practice area lead for a project",
        rank=2,
    )
    PermissionType.objects.create(
        name=member_project, description="Project team member", rank=3
    )


def reverse(__code__, __reverse_code__):
    PermissionType.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ("data", "0003_sdg_seed"),
        ("core", "0023_event_could_attend_event_must_attend_and_more"),
    ]

    operations = [migrations.RunPython(forward, reverse)]
