from django.db import migrations

from core.models import Sdg


def run(__code__, __reverse_code__):
    items = [
        (1, "No Poverty", "End poverty in all its forms everywhere", "sdg01.png"),
        (2, "Zero Hunger", "End hunger, achieve food security and improved nutrition and promote sustainable agriculture", "sdg02.png"),
        (3, "Good Heath and Well-Being", "Ensure healthy lives and promote well-being for all at all ages", "sdg03.png"),
        (4, "Quality Education", "Ensure inclusive and equitable quality education and promote lifelong learning opportunities for all", "sdg04.png"),
        (5, "Gender Equality", "Achieve gender equality and empower all women and girls", "sdg05.png"),
        (6, "Clean Water and Sanitation", "Ensure availability and sustainable management of water and sanitation for all", "sdg06.png"),
        (7, "Affordable and Clean Energy", "Ensure access to affordable, reliable, sustainable and modern energy for all", "sdg07.png"),
        (8, "Decent Work and Economic Growth", "Promote sustained, inclusive and sustainable economic growth, full and productive employment and decent work for all", "sdg08.png"),
        (9, "Industry Innovation and Infrastructure", "Build resilient infrastructure, promote inclusive and sustainable industrialization and foster innovation", "sdg09.png"),
        (10, "Reduced Inequalties", "Reduce inequality within and among countries", "sdg10.png"),
        (11, "Sustainable Cities and Communities", "Make cities and human settlements inclusive, safe, resilient and sustainable", "sdg11.png"),
        (12, "Responsible Consumption and Production", "Ensure sustainable consumption and production patterns", "sdg12.png"),
        (13, "Climate Action", "Take urgent action to combat climate change and its impacts [n 10]", "sdg13.png"),
        (14, "Life Below Water", "Conserve and sustainably use the oceans, seas and marine resources for sustainable development", "sdg14.png"),
        (15, "Life on Land", "Protect, restore and promote sustainable use of terrestrial ecosystems, sustainably manage forests, combat desertification, and halt and reverse land degradation and halt biodiversity loss", "sdg15.png"),
        (16, "Peace, Justice and Strong Institutions", "Promote peaceful and inclusive societies for sustainable development, provide access to justice for all and build effective, accountable and inclusive institutions at all levels", "sdg16.png"),
        (17, "Partnerships for The Goals", "Strengthen the means of implementation and revitalize the Global Partnership for Sustainable Development", "sdg17.png"),
    ]
    for uuid, name, description, image in items:
        Sdg.objects.create(uuid=uuid, name=name, description=description, image=image)


class Migration(migrations.Migration):
    initial = True
    dependencies = [("data", "0002_practicearea_seed")]


operations = [migrations.RunPython(run, migrations.RunPython.noop)]
