
from django.db import migrations
from core.scripts.programarea_seed import run as run_seed

   
class Migration(migrations.Migration):

    initial = True
    dependencies = [
        ('core', '0001_initial')
    ]

    operations = [
        migrations.RunPython(run_seed, migrations.RunPython.noop)
    ]
        
        
