from django.db import migrations

from core.models import CheckType


def forward(__code__, __reverse_code__):
    items = [
        (1, "GitHub Invite Acepted", ""),
        (2, "Slack Invite Accepted", ""),
        (3, "2FA setup", ""),
        (4, "Google Calendar invite Accepted", ""),
        (5, "GitHub membership public", ""),
        (6, "Accepted Code of Conduct", ""),
    ]
    for uuid, name, description in items:
        CheckType.objects.create(uuid=uuid, name=name, description=description)


def reverse(__code__, __reverse_code__):
    CheckType.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [("data", "0004_permissiontype_seed")]

    operations = [migrations.RunPython(forward, reverse)]
