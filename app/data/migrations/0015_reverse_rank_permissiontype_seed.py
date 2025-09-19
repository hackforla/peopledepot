from django.db import migrations
from core.models import PermissionType


def reverse_and_multiply_ranks(apps, schema_editor):
    for pt in PermissionType.objects.all():
        pt.rank = (9 - pt.rank) * 10
        pt.save(update_fields=["rank"])


def revert_ranks(apps, schema_editor):
    for pt in PermissionType.objects.all():
        pt.rank = 9 - (pt.rank // 10)
        pt.save(update_fields=["rank"])


class Migration(migrations.Migration):

    dependencies = [
        ("data", "0014_socminor_seed"),
    ]

    operations = [
        migrations.RunPython(reverse_and_multiply_ranks, reverse_code=revert_ranks),
    ]
