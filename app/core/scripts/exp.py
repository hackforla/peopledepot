from core.models import Expirement


def run():

    status = Expirement(uuid=2, quanity="13")
    status.save()
