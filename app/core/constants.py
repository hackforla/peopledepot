practice_area_lead = "PracticeAreaLead"
global_admin = "GlobalAdmin"
project_team_member = "ProjectTeamMember"
practice_area_team_member = "PracticeAreaTeamMember"
verified_user = "VerifiedUser"
project_lead = "ProjectLead"

class PermissionTypeValue:
    practice_area_lead = "PracticeAreaLead"
    global_admin = "GlobalAdmin"
    project_team_member = "ProjectTeamMember"
    practice_area_team_member = "PracticeAreaTeamMember"
    verified_user = "VerifiedUser"
    project_lead = "ProjectLead"

read_fields = {
    "user": {
        "secure": (
            "uuid",
            "username",
            "created_at",
            "updated_at",
            "email",
            "first_name",
            "last_name",
            "gmail",
            "preferred_email",
            "current_job_title",
            "target_job_title",
            "current_skills",
            "target_skills",
            "linkedin_account",
            "github_handle",
            "slack_id",
            "phone",
            "texting_ok",
            "time_zone",
        ),
        "basic": ("username", "slack_id", "first_name", "last_name"),
    },
}
