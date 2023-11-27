from core.models import PracticeArea


def run(__state_apps__, __schema_editor__):
    status = PracticeArea(uuid=1, name="Development")
    status.save()
    status = PracticeArea(uuid=2, name="Project Management")
    status.save()
    status = PracticeArea(uuid=3, name="Design")
    status.save()
    status = PracticeArea(uuid=4, name="Professional Development")
    status.save()
