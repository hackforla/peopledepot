# Generated by Django 4.2.11 on 2024-05-19 02:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0023a_permissionassignment"),
    ]

    operations = [
        migrations.AlterField(
            model_name="permissionassignment",
            name="practiceArea",
            field=models.ForeignKey(
                blank=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="core.practicearea",
            ),
        ),
        migrations.AlterField(
            model_name="permissionassignment",
            name="project",
            field=models.ForeignKey(
                blank=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="core.project",
            ),
        ),
    ]