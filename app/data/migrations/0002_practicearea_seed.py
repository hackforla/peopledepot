
from django.db import migrations
from core.scripts.practicearea_seed import run

   
class Migration(migrations.Migration):

    initial = True
    dependencies = [
        ('data', '0001_programarea_seed')
    ]

    operations = [
        migrations.RunPython(run, migrations.RunPython.noop)
    ]
        
        
