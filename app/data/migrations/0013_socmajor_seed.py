from django.db import migrations

from core.models import SocMajor


def forward(__code__, __reverse_code__):
    items = [
        (11, "31-0000", "Healthcare Support Occupations"),
        (12, "33-0000", "Protective Service Occupations"),
        (13, "35-0000", "Food Preparation and Serving Related Occupations"),
        (14, "37-0000", "Building and Grounds Cleaning and Maintenance Occupations"),
        (15, "39-0000", "Personal Care and Service Occupations"),
        (16, "41-0000", "Sales and Related Occupations"),
        (17, "43-0000", "Office and Administrative Support Occupations"),
        (18, "45-0000", "Farming, Fishing, and Forestry Occupations"),
        (19, "47-0000", "Construction and Extraction Occupations"),
        (20, "49-0000", "Installation, Maintenance, and Repair Occupations"),
        (21, "51-0000", "Production Occupations"),
        (22, "53-0000", "Transportation and Material Moving Occupations"),
    ]
    for uuid, occ_code, title in items:
        SocMajor.objects.create(uuid=uuid, occ_code=occ_code, title=title)


def reverse(__code__, __reverse_code__):
    SocMajor.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [("data", "0012_leadershiptype_seed")]

    operations = [migrations.RunPython(forward, reverse)]
