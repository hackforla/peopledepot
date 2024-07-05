from constants import global_admin, practice_area_admin, project_team_member, project_lead


def _get_fields(field_privs, crud_priv):
    ret_array = []
    for key, value in field_privs.items():
        if crud_priv in value:
            ret_array.append(key)
    return ret_array


def self_register_field_permissions():
    return {
        "username",
        "first_name",
        "last_name",
        "gmail",
        "preferred_email",
        "linkedin_account",
        "github_handle",
        "phone",
        "texting_ok",
        # "intake_current_job_title": "CR",
        # "intake_target_job_title": "CR",
        "current_job_title",
        "target_job_title",
        # "intake_current_skills": "CR",
        # "intake_target_skills": "CR",
        "current_skills",
        "target_skills",
        "time_zone",
    }


def me_field_permissions():
    return {
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
        "gmail": "RU",
        "preferred_email": "RU",
        "linkedin_account": "RU",
        "github_handle": "RU",
        "phone": "RU",
        "texting_ok": "RU",
        # "intake_current_job_title": "CR",
        # "intake_target_job_title": "CR",
        "current_job_title": "RU",
        "target_job_title": "RU",
        # "intake_current_skills": "CR",
        # "intake_target_skills": "CR",
        "current_skills": "RU",
        "target_skills": "RU",
        "time_zone": "R",
    }


def _user_field_permissions():
    permissions = {project_team_member: {}, practice_area_admin: {}, global_admin: {}}

    permissions[project_team_member] = {
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
        "time_zone": "R",
    }

    permissions[practice_area_admin] = {
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
        "gmail": "RU",
        "preferred_email": "RU",
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
        "time_zone": "R",
    }
    
    permissions[project_lead] = permissions[practice_area_admin].copy()

    permissions[global_admin] = {
        "uuid": "R",
        "created_at": "R",
        "updated_at": "R",
        "is_superuser": "CRU",
        "is_active": "CRU",
        "is_staff": "CRU",
        # "is_verified": "CRU",
        "username": "CRU",
        "first_name": "CRU",
        "last_name": "CRU",
        "gmail": "CRU",
        "preferred_email": "CRU",
        "linkedin_account": "CRU",
        "github_handle": "CRU",
        "phone": "RU",
        "texting_ok": "CRU",
        # "intake_current_job_title": "CRU",
        # "intake_target_job_title": "CRU",
        "current_job_title": "CRU",
        "target_job_title": "CRU",
        # "intake_current_skills": "CRU",
        # "intake_target_skills": "CRU",
        "current_skills": "CRU",
        "target_skills": "CRU",
        "time_zone": "CR",
    }
    return permissions


class UserCruPermissions:
    permissions = _user_field_permissions()

    _read_fields_for_project_lead = _get_fields(
        permissions[project_lead], "R"
    )
    _read_fields_for_practice_area_admin = _get_fields(
        permissions[practice_area_admin], "R"
    )
    _read_fields_for_project_team_member = _get_fields(
        permissions[project_team_member], "R"
    )
    _read_fields_for_global_admin = _get_fields(permissions[global_admin], "R")
    read_fields = {
        project_lead: _read_fields_for_project_lead,
        project_team_member: _read_fields_for_project_team_member,
        practice_area_admin: _read_fields_for_practice_area_admin,
        global_admin: _read_fields_for_global_admin,
    }

    _update_fields_for_practice_area_admin = _get_fields(
        permissions[practice_area_admin], "U"
    )
    _update_fields_for_project_team_member = _get_fields(
        permissions[project_team_member], "U"
    )
    _update_fields_for_global_admin = _get_fields(permissions[global_admin], "U")
    update_fields = {
        practice_area_admin: _update_fields_for_practice_area_admin,
        project_team_member: _update_fields_for_project_team_member,
        global_admin: _update_fields_for_global_admin,
    }
