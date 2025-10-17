from django.db import migrations

from core.models import PermissionType


def insert_data(__code__, __reverse_code__):
    items = [
        (1, "adminGlobal", "Granted to People Depo Admins. Can CRUD anything.", 1),
        (
            2,
            "adminVrms",
            "Granted to VRMS the application.  Can R anything and update permissions for users to the level of Admin Brigade",
            2,
        ),
        (
            3,
            "adminBrigade",
            "Granted to Brigage Leads.  Can CRUD anything related to a user or project assigned to their brigade ",
            3,
        ),
        (
            4,
            "adminProject",
            "Granted to Product Managers.  Can Read and Update anything related to their assigned project",
            4,
        ),
        (
            5,
            "practiceLeadProject",
            "Granted when a user is promoted or assigned to be a Project Lead.  Can R and U anything related to people in their practice area (must attend lead events)",
            5,
        ),
        (
            6,
            "practiceLeadJrProject",
            "Granted when a user is promoted or assigned to be a Jr Project Lead.  Can R and U anything related to people in their practice area (should attend lead events)",
            6,
        ),
        (
            7,
            "memberProject",
            "Granted when a user joins a project.  Can Read anything related to their project that is visible",
            7,
        ),
        (
            8,
            "memberGeneral",
            "Granted when a user finishes onboaring.  Can express interest in a project's open role if they are the role",
            8,
        ),
    ]
    for uuid, name, description, rank in items:
        PermissionType.objects.create(
            uuid=uuid, name=name, description=description, rank=rank
        )


def clear_table(__code__, __reverse_code__):
    PermissionType.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ("data", "0003_sdg_seed"),
        ("core", "0026_permissiontype_rank_alter_permissiontype_name_and_more"),
    ]

    operations = [migrations.RunPython(insert_data, clear_table)]
