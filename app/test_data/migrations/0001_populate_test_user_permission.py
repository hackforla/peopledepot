# app/test_data/migrations/0001_populate_test_user_permission.py
from django.db import migrations


def load_test_data(apps, schema_editor):
    _ = apps, schema_editor  # Unused
    from ..utils.load_data import load_data
    from django.db import connections

    for alias in connections:
        name = connections[alias].settings_dict["NAME"]
        if name.startswith("test_"):
            load_data()
            break


class Migration(migrations.Migration):
    dependencies = [("data", "0014_socminor_seed")]
    operations = [
        migrations.RunPython(load_test_data),
    ]
