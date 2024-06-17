from django.db import migrations

from core.models import ProgramArea


def forward(__code__, __reverse_code__):
    items = [
        (1, "Citizen Engagement"),
        (2, "Civic Tech Infrastructure"),
        (3, "Diversity / Equity and Inclusion"),
        (4, "Environment"),
        (5, "Justice"),
        (6, "Social Safety Net"),
        (7, "Vote / Representation"),
        (8, "Workforce Development"),
        (9, "Community of Practice"),
    ]
    for uuid, name in items:
        ProgramArea.objects.create(uuid=uuid, name=name)


def reverse(__code__, __reverse_code__):
    ProgramArea.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [("core", "0018_rename_recurringevent_event")]

    operations = [migrations.RunPython(forward, reverse)]
