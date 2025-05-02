from django.db import migrations

from core.models import ReferrerType


def forward(__code__, __reverse_code__):
    items = [
        ("Bootcamp", ""),
        ("College Career Center", ""),
        ("Mentor", ""),
        ("Friend", ""),
        ("Active Volunteer", ""),
        ("Inactive Volunteer", ""),
    ]
    for name, description in items:
        ReferrerType.objects.create(name=name, description=description)


def reverse(__code__, __reverse_code__):
    ReferrerType.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [("data", "0010_eventtype_seed")]

    operations = [migrations.RunPython(forward, reverse)]
