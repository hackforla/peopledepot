from django.db import migrations

from core.models import ProgramArea

<<<<<<< HEAD
def run(__code__, __reverse_code__):
    status = ProgramArea(id=1, name="Citizen Engagement")
    status.save()
    status = ProgramArea(id=2, name="Civic Tech Infrastructure")
    status.save()
    status = ProgramArea(id=3, name="Diversity / Equity and Inclusion")
    status.save()
    status = ProgramArea(id=4, name="Environment")
    status.save()
    status = ProgramArea(id=5, name="Justice")
    status.save()
    status = ProgramArea(id=6, name="Social Safety Net")
    status.save()
    status = ProgramArea(id=7, name="Vote / Representation")
    status.save()
    status = ProgramArea(id=8, name="Workforce Development")
    status.save()
    status = ProgramArea(id=9, name="Community of Practice")
    status.save()
   
=======

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


>>>>>>> main
class Migration(migrations.Migration):
    initial = True
    dependencies = [("core", "0018_rename_recurringevent_event")]

    operations = [migrations.RunPython(run, migrations.RunPython.noop)]
