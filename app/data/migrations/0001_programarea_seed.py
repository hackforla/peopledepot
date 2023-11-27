from django.db import migrations
from core.scripts.programarea_seed import run


class Migration(migrations.Migration):
    initial = True
    dependencies = [("core", "0018_rename_recurringevent_event")]

    operations = [migrations.RunPython(run, migrations.RunPython.noop)]
