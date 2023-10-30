from core.models import ProgramArea


def run():

    status = ProgramArea(uuid="1", name="Citizen Engagement")
    status.save()
    status = ProgramArea(uuid="2", name="Civic Tech Infrastructure")
    status.save()
    status = ProgramArea(uuid="3", name="Diversity / Equity and Inclusion")
    status.save()
    status = ProgramArea(uuid="4", name="Environment")
    status.save()
    status = ProgramArea(uuid="5", name="Justice")
    status.save()
    status = ProgramArea(uuid="6", name="Social Safety Net")
    status.save()
    status = ProgramArea(uuid="7", name="Vote / Representation")
    status.save()
    status = ProgramArea(uuid="8", name="Workforce Development")
    status.save()
    status = ProgramArea(uuid="9", name="Community of Practice")
    status.save()
