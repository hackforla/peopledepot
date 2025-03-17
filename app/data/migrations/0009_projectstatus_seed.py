from django.db import migrations

from core.models import ProjectStatus


def forward(__code__, __reverse_code__):
    items = [
        ("Active", "Has a project team and current meetings"),
        ("On Hold", "No project team or meetings scheduled "),
        ("Completed", "Project is completed"),
        (
            "Closed",
            "Closed, possibly not completed (usually does not show up on the website).  Unlikely to be reopened.",
        ),
        (
            "Deleted",
            "Holds for 90 days before final removal (used for test project entries, or mistakes that do not need to be remembered)",
        ),
    ]
    for name, description in items:
        ProjectStatus.objects.create(name=name, description=description)


def reverse(__code__, __reverse_code__):
    ProjectStatus.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [("data", "0008_userstatustype_seed")]

    operations = [migrations.RunPython(forward, reverse)]
