from django.db import migrations

from core.models import LeadershipType


def forward(__code__, __reverse_code__):
    items = [
        ("Mentor Led", "Has a mentor in a leadership role"),
        ("Peer Led", "Peers run the meetings"),
        ("Community Led", "Community members run the meetings"),
        ("Product Led", "Projects"),
    ]
    for name, description in items:
        LeadershipType.objects.create(name=name, description=description)


def reverse(__code__, __reverse_code__):
    LeadershipType.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [("data", "0011_referrertype_seed")]

    operations = [migrations.RunPython(forward, reverse)]
