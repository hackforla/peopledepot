class PermissionValue:
    practice_area_admin = "PracticeAreaAdmin"
    global_admin = "GlobalAdmin"
    project_team_member = "ProjectTeamMember"
    practice_area_team_member = "PracticeAreaTeamMember"
    verified_user = "VerifiedUser"
    project_admin = "ProjectAdmin"
    basic = "basic"


class Fields:
    read = {
        "user": {
            PermissionValue.global_admin: (
                "uuid",
                "username",
                "created_at",
                "updated_at",
                "email",
                "first_name",
                "last_name",
                "linkedin_account",
                "github_handle",
                "slack_id",
                "phone",
                "texting_ok",
            ),
            PermissionValue.basic: ("username", "slack_id", "first_name", "last_name"),
        },
    }
    update = {
        "user": {
            PermissionValue.global_admin: (
                "uuid",
                "username",
                "email",
                "first_name",
                "last_name",
                "linkedin_account",
                "github_handle",
                "slack_id",
                "phone",
                "texting_ok",
            ),
            PermissionValue.project_admin: (
                "uuid",
                "username",
                "first_name",
                "last_name",
                "linkedin_account",
                "github_handle",
                "slack_id",
                "phone",
                "texting_ok",
                "time_zone",
            ),
            PermissionValue.basic: ("username", "slack_id", "first_name", "last_name"),
        },
    }
