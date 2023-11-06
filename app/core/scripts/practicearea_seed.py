from core.models import PracticeArea

def run(_a, _b):

    status = PracticeArea(uuid=1, name="Development")
    status.save()
    status = PracticeArea(uuid=2, name="Project Management")
    status.save()
    status = PracticeArea(uuid=3, name="Design")
    status.save()
    status = PracticeArea(uuid=4, name="Professional Development")
    status.save()
