# Generated by Django 4.2.11 on 2024-11-12 20:15

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [("core", "0031_userstatustype_user_user_status")]

    operations = [
        migrations.CreateModel(
            name="ProjectProgramAreaXref",
            fields=[
                (
                    "uuid",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="Created at"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="Updated at"),
                ),
                (
                    "program_area",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core.programarea",
                    ),
                ),
                (
                    "project",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="core.project"
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.AddField(
            model_name="project",
            name="program_areas",
            field=models.ManyToManyField(
                blank=True,
                related_name="projects",
                through="core.ProjectProgramAreaXref",
                to="core.programarea",
            ),
        ),
    ]
