from django.db import migrations

from constants import PRACTICE_AREA_ADMIN, PROJECT_LEAD
from core.models import PermissionType, Sdg


def forward(__code__, __reverse_code__):
    PermissionType.objects.create(name=PROJECT_LEAD, description="Project Lead")
    PermissionType.objects.create(
        name=PRACTICE_AREA_ADMIN, description="Practice Area Admin"
    )


def reverse(__code__, __reverse_code__):
    PermissionType.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [("data", "0003_sdg_seed")]

    operations = [migrations.RunPython(forward, reverse)]
