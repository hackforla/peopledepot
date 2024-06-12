from django.db import migrations

from core.models import PermissionType


def run(__code__, __reverse_code__):
    items = [
        (1, "adminGlobal", "Granted to People Depo Admins. Can CRUD anything."),
        (
            2,
            "adminVrms",
            "Granted to VRMS the application.  Can R anything and update permissions for users to the level of Admin Brigade",
        ),
        (
            3,
            "adminBrigade",
            "Granted to Brigage Leads.  Can CRUD anything related to a user or project assigned to their brigade ",
        ),
        (
            4,
            "adminProject",
            "Granted to Product Managers.  Can Read and Update anything related to their assigned project",
        ),
        (
            5,
            "practiceLeadProject",
            "Granted when a user is promoted or assigned to be a Project Lead.  Can R and U anything related to people in their practice area (must attend lead events)",
        ),
        (
            6,
            "practiceLeadJrProject",
            "Granted when a user is promoted or assigned to be a Jr Project Lead.  Can R and U anything related to people in their practice area (should attend lead events)",
        ),
        (
            7,
            "memberProject",
            "Granted when a user joins a project.  Can Read anything related to their project that is visible",
        ),
        (
            8,
            "memberGeneral",
            "Granted when a user finishes onboaring.  Can express interest in a project's open role if they are the role",
        ),
    ]
    for uuid, name, description in items:
        PermissionType.objects.create(uuid=uuid, name=name, description=description)


class Migration(migrations.Migration):
    initial = True
    dependencies = [("data", "0003_sdg_seed")]


operations = [migrations.RunPython(run, migrations.RunPython.noop)]
