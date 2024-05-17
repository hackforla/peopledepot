from django.db import migrations
from core.models import PracticeArea


def run(__code__, __reverse_code__):
    status = PracticeArea(uuid=1, name="Development")
    status.save()
    status = PracticeArea(uuid=2, name="Project Management")
    status.save()
    status = PracticeArea(uuid=3, name="Design")
    status.save()
    status = PracticeArea(uuid=4, name="Professional Development")
    status.save()


class Migration(migrations.Migration):
    initial = True
    dependencies = [("data", "0001_programarea_seed")]

    operations = [migrations.RunPython(run, migrations.RunPython.noop)]


from django.db import migrations
from core.models import PracticeArea


def run(__code__, __reverse_code__):
    START_WITH = 1000
    items = [
        (1 + START_WITH, "Development"),
        (2 + START_WITH, "Project Management"),
        (3 + START_WITH, "Design"),
        (4 + START_WITH, "Professional Development"),
    ]
    for uuid, name in items:
        PracticeArea.objects.create(uuid=uuid, name=name)


class Migration(migrations.Migration):
    initial = True
    dependencies = [("data", "0001_programarea_seed")]

    operations = [migrations.RunPython(run, migrations.RunPython.noop)]
