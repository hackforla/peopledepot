from django.db import migrations

from core.models import ProgramArea


def run(__code__, __reverse_code__):
    START_WITH = 1000
    items = [
        (1 + START_WITH, "Citizen Engagement"),
        (2 + START_WITH, "Civic Tech Infrastructure"),
        (3 + START_WITH, "Diversity / Equity and Inclusion"),
        (4 + START_WITH, "Environment"),
        (5 + START_WITH, "Justice"),
        (6 + START_WITH, "Social Safety Net"),
        (7 + START_WITH, "Vote / Representation"),
        (8 + START_WITH, "Workforce Development"),
        (9 + START_WITH, "Community of Practice"),
    ]
    for program_id, name in items:
        ProgramArea.objects.create(id=program_id, name=name)


class Migration(migrations.Migration):
    initial = True
    dependencies = [("core", "0018_rename_recurringevent_event")]

    operations = [migrations.RunPython(run, migrations.RunPython.noop)]
