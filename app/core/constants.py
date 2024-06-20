#
class PermissionValue:
    practice_area_lead = "PracticeAreaAdmin"
    global_admin = "GlobalAdmin"
    project_team_member = "ProjectTeamMember"
    project_admin = "ProjectAdmin"
    self_value = "Self"


_global_admin = PermissionValue.global_admin
_practice_area_lead = PermissionValue.practice_area_lead
_project_team_member = PermissionValue.project_team_member
_self_value = PermissionValue.self_value


def get_fields(field_privs, crud_priv):
    ret_array = []
    for key, value in field_privs.items():
        if crud_priv in value:
            ret_array.append(key)
    return ret_array


def get_field_permissions():
    permissions = {
        "user": {
            _self_value: {},
            _project_team_member: {},
            _practice_area_lead: {},
            _global_admin: {},
        }
    }

    permissions["user"][_self_value] = {
        "uuid": "R",
        "created_at": "R",
        "updated_at": "R",
        "is_superuser": "R",
        "is_active": "R",
        "is_staff": "R",
        # "is_verified": "R",
        "username": "R",
        "first_name": "CRU",
        "last_name": "CRU",
        "gmail": "CRU",
        "preferred_email": "CRU",
        "linkedin_account": "CRU",
        "github_handle": "CRU",
        "phone": "CRU",
        "texting_ok": "CRU",
        # "intake_current_job_title": "CR",
        # "intake_target_job_title": "CR",
        "current_job_title": "CRU",
        "target_job_title": "CRU",
        # "intake_current_skills": "CR",
        # "intake_target_skills": "CR",
        "current_skills": "CRU",
        "target_skills": "CRU",
    }
    permissions["user"][_project_team_member] = {
        "uuid": "R",
        "created_at": "R",
        "updated_at": "R",
        "is_superuser": "R",
        "is_active": "R",
        "is_staff": "R",
        # "is_verified": "R",
        "username": "R",
        "first_name": "R",
        "last_name": "R",
        "gmail": "R",
        "preferred_email": "R",
        "linkedin_account": "R",
        "github_handle": "R",
        "phone": "X",
        "texting_ok": "X",
        # "intake_current_job_title": "R",
        # "intake_target_job_title": "R",
        "current_job_title": "R",
        "target_job_title": "R",
        # "intake_current_skills": "R",
        # "intake_target_skills": "R",
        "current_skills": "R",
        "target_skills": "R",
    }

    permissions["user"][_practice_area_lead] = {
        "uuid": "R",
        "created_at": "R",
        "updated_at": "R",
        "is_superuser": "R",
        "is_active": "R",
        "is_staff": "R",
        # "is_verified": "R",
        "username": "R",
        "first_name": "RU",
        "last_name": "RU",
        "gmail": "R",
        "preferred_email": "R",
        "linkedin_account": "RU",
        "github_handle": "RU",
        "phone": "RU",
        "texting_ok": "RU",
        # "intake_current_job_title": "R",
        # "intake_target_job_title": "R",
        "current_job_title": "R",
        "target_job_title": "R",
        # "intake_current_skills": "R",
        # "intake_target_skills": "R",
        "current_skills": "R",
        "target_skills": "R",
    }

    permissions["user"][_global_admin] = {
        "uuid": "R",
        "created_at": "R",
        "updated_at": "R",
        "is_superuser": "CRU",
        "is_active": "CRU",
        "is_staff": "CRU",
        # "is_verified": "CRU",
        "username": "CRU",
        "first_name": "RU",
        "last_name": "RU",
        "gmail": "CRU",
        "preferred_email": "CRU",
        "linkedin_account": "RU",
        "github_handle": "RU",
        "phone": "RU",
        "texting_ok": "RU",
        # "intake_current_job_title": "CRU",
        # "intake_target_job_title": "CRU",
        "current_job_title": "CRU",
        "target_job_title": "CRU",
        # "intake_current_skills": "CRU",
        # "intake_target_skills": "CRU",
        # "current_skills": "CRU",
        "target_skills": "CRU",
    }
    return permissions


class FieldPermissions:
    permissions = get_field_permissions()

    _read_fields_for_self = get_fields(permissions["user"][_self_value], "R")
    _read_fields_for_practice_area_lead = get_fields(
        permissions["user"][_practice_area_lead], "R"
    )
    _read_fields_for_project_team_member = get_fields(
        permissions["user"][_project_team_member], "R"
    )
    _read_fields_for_global_admin = get_fields(permissions["user"][_global_admin], "R")
    read_fields = {
        "user": {
            _self_value: _read_fields_for_self,
            _project_team_member: _read_fields_for_project_team_member,
            _practice_area_lead: _read_fields_for_practice_area_lead,
            _global_admin: _read_fields_for_global_admin,
        }
    }

    _update_fields_for_self = get_fields(permissions["user"][_self_value], "U")
    _update_fields_for_practice_area_lead = get_fields(
        permissions["user"][_practice_area_lead], "U"
    )
    _update_fields_for_project_team_member = get_fields(
        permissions["user"][_project_team_member], "U"
    )
    _update_fields_for_global_admin = get_fields(
        permissions["user"][_global_admin], "U"
    )
    update_fields = {
        "user": {
            _self_value: _update_fields_for_self,
            _practice_area_lead: _update_fields_for_practice_area_lead,
            _project_team_member: _update_fields_for_project_team_member,
            _global_admin: _update_fields_for_global_admin,
        }
    }
    print("debug update fields", update_fields)
