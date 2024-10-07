from django.db import migrations

from core.models import UrlType


def forward(__code__, __reverse_code__):
    items = [
        (1, "Readme", "The GitHub readme.md file for the project"),
        (
            2,
            "HfLA Website",
            "The URL of the project's page on the hackforla.org website",
        ),
        (3, "GitHub", "Project's primary GitHub repo"),
        (4, "Slack", "Project's slack channel"),
        (5, "Google Drive", "The url to the project Google Drive"),
        (6, "Wiki", "The wiki for the project"),
        (7, "Test Site", "Development site used for testing"),
        (
            8,
            "Demo Site",
            "Website used for public demonstration - usually with fake data. Primarily used by projects that don't have a live site yet.",
        ),
        (9, "Site", "Live on the internet such as https://example.com "),
        (10, "Overview", "The Project One sheet"),
        (11, "Other", ""),
    ]
    for uuid, name, description in items:
        UrlType.objects.create(uuid=uuid, name=name, description=description)


def reverse(__code__, __reverse_code__):
    UrlType.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [("data", "0006_socmajor_seed")]

    operations = [migrations.RunPython(forward, reverse)]
