from django.db import migrations

from core.models import SocMajor


def forward(__code__, __reverse_code__):
    items = [
        (1, "11-2000", "Management Occupations"),
        (2, "13-0000", "Business and Financial Operations Occupations"),
        (3, "15-0000", "Computer and Mathematical Occupations"),
        (4, "17-0000", "Architecture and Engineering Occupations"),
        (5, "19-0000", "Life, Physical, and Social Science Occupations"),
        (6, "21-0000", "Community and Social Service Occupations"),
        (7, "23-0000", "Legal Occupations"),
        (8, "25-0000", "Educational Instruction and Library Occupations"),
        (9, "27-0000", "Arts, Design, Entertainment, Sports, and Media Occupations"),
        (10, "29-0000", "Healthcare Practitioners and Technical Occupations"),
    ]
    for uuid, occ_code, title in items:
        SocMajor.objects.create(uuid=uuid, occ_code=occ_code, title=title)


def reverse(__code__, __reverse_code__):
    SocMajor.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [("data", "0005_checktype_seed")]

    operations = [migrations.RunPython(forward, reverse)]
