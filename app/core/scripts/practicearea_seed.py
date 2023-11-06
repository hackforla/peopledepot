from core.models import PracticeArea

def run(_a, _b):

    status = PracticeArea(uuid=1, name="Citizen Engagement")
    status.save()
    status = PracticeArea(uuid=2, name="Civic Tech Infrastructure")
    status.save()
    status = PracticeArea(uuid=3, name="Diversity / Equity and Inclusion")
    status.save()
    status = PracticeArea(uuid=4, name="Environment")
    status.save()
    status = PracticeArea(uuid=5, name="Justice")
    status.save()
    status = PracticeArea(uuid=6, name="Social Safety Net")
    status.save()
    status = PracticeArea(uuid=7, name="Vote / Representation")
    status.save()
    status = PracticeArea(uuid=8, name="Workforce Development")
    status.save()
    status = PracticeArea(uuid=9, name="Community of Practice")
    status.save()
