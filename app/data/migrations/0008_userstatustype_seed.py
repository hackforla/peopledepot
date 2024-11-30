from django.db import migrations

from core.models import UserStatusType


def forward(__code__, __reverse_code__):
    items = [
        (
            1,
            "Inactive",
            "Member who has not checked into their project or Community of Practice for 4 weeks and does not have a timeAwayHold",
        ),
        (2, "Active", "Member that is checking into meetings"),
        (
            3,
            "Time Away Hold",
            "Hold placed by the member or their leader after they have announced a temporary absence",
        ),
        (4, "Barred", "Member who has been removed from the community"),
    ]
    for uuid, name, description in items:
        UserStatusType.objects.create(uuid=uuid, name=name, description=description)


def reverse(__code__, __reverse_code__):
    UserStatusType.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [("data", "0007_urltype_seed")]

    operations = [migrations.RunPython(forward, reverse)]
