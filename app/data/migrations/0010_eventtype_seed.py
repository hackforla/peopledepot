from django.db import migrations

from core.models import EventType


def forward(__code__, __reverse_code__):
    items = [
        ("Team Meeting", ""),
        ("Onboarding", ""),
        ("Mixer", ""),
        ("Special Event", ""),
        ("Community of Practice", ""),
    ]
    for name, description in items:
        EventType.objects.create(name=name, description=description)
    pass


def reverse(__code__, __reverse_code__):
    EventType.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [("data", "0009_projectstatus_seed")]

    operations = [migrations.RunPython(forward, reverse)]
