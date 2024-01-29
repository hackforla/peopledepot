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
    items = [
        (1, "Development"),
        (2, "Project Management"),
        (3, "Design"),
        (4, "Professional Development"),
    ]
    for uuid, name in items:
        PracticeArea.objects.create(uuid=uuid, name=name)


class Migration(migrations.Migration):
    initial = True
    dependencies = [("data", "0001_programarea_seed")]

    operations = [migrations.RunPython(run, migrations.RunPython.noop)]
