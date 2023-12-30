from django.db import migrations

from core.models import ProgramArea


def run(__code__, __reverse_code__):
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


class Migration(migrations.Migration):
    initial = True
    dependencies = [("core", "0018_rename_recurringevent_event")]

    operations = [migrations.RunPython(run, migrations.RunPython.noop)]
