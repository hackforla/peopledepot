from core.models import UserStatus

def run():

    status = UserStatus(name="Inactive", description="Member who has not checked into their project or Community of Practice for 4 weeks and does not have a timeAwayHold")
    status.save()
    status = UserStatus(name="Active", description="Member that is checking into meetings")
    status.save()
    status = UserStatus(name="Time Away Hold", description="Hold placed by the member or their leader after they have announced a temporary absence")
    status.save()
    status = UserStatus(name="Barred", description="Member who has been removed from the community")
    status.save()
