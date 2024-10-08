from constants import admin_global
from constants import admin_project
from constants import member_project
from constants import practice_lead_project

profile_value = "profile"

_cru_permissions = {
    member_project: {},
    practice_lead_project: {},
    admin_project: {},
    admin_global: {},
    profile_value: {},
}

# permissions for the "me" endpoint which is used for the user to view and
# patch their own information
_cru_permissions[profile_value] = {
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


# permissions for the user endpoint which is used for creating, viewing, and updating
# based on assigned permission type

_cru_permissions[member_project] = {
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
    # "target_job_title": "R",
    # "intake_current_skills": "R",
    # "intake_target_skills": "R",
    "current_skills": "R",
    # "target_skills": "R",
    "time_zone": "R",
}

_cru_permissions[practice_lead_project] = {
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

_cru_permissions[admin_project] = _cru_permissions[practice_lead_project].copy()

_cru_permissions[admin_global] = {
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
    "email": "CRU",
    "slack_id": "CRU",
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
    "password": "CU",
}


def _get_fields_with_priv(field_permissions, cru_permission):
    ret_array = []
    for key, value in field_permissions.items():
        if cru_permission in value:
            ret_array.append(key)
    return ret_array


class Cru:
    """Variables that define the fields that can be read or updated by a user based on user permissionss

    Variables:


        Cru.user_read_fields:
            Cru.user_read_fields[admin_global]: list of fields a global admin can read for a user
            Cru.user_read_fields[admin_project]: list of fields a project lead can read for a user
            Cru.user_read_fields[member_project]: list of fields a project member can read for a user
            Cru.user_read_fields[practice_lead_project]: list of fields a practice area admin can read for a user
            Cru.user_read_fields[profile_value]: list of fields a user can read when using /me (profile) endpoint
        Cru.user_patch_fields:
            Cru.user_patch_fields[admin_global]: list of fields a global admin can update for a user
            Cru.user_patch_fields[admin_project]: list of fields a project lead can update for a user
            Cru.user_patch_fields[member_project]: list of fields a project member can update for a user
            Cru.user_patch_fields[practice_lead_project]: list of fields a practice area admin can update for a user
            Cru.user_patch_fields[profile_value]: list of fields a user can update when using /me (profile) endpoint
        Cru.user_post_fields:
            Cru.user_post_fields[admin_global]: list of fields a global admin can specify when creating a user
    """

    user_read_fields = {
        admin_global: (),
        admin_project: (),
        practice_lead_project: (),
        member_project: (),
        profile_value: (),
    }

    user_patch_fields = {
        admin_global: (),
        admin_project: (),
        practice_lead_project: (),
        member_project: (),
        profile_value: (),
    }

    user_post_fields = {
        admin_global: (),
        admin_project: (),
        practice_lead_project: (),
        member_project: (),
        profile_value: (),
    }


def _derive_user_priv_fields():
    """
    Populates following attributes based on values in UserFieldPermissions
    - Cru.user_post_fields
    - Cru.user_patch_fields
    - Cru.user_post_fields
    -  me_endpoint_read_fields
    -  me_endpoint_patch_fields
    """
    for permission_type in [
        admin_project,
        member_project,
        practice_lead_project,
        admin_global,
        profile_value,
    ]:
        Cru.user_read_fields[permission_type] = _get_fields_with_priv(
            _cru_permissions[permission_type], "R"
        )

        Cru.user_patch_fields[permission_type] = _get_fields_with_priv(
            _cru_permissions[permission_type], "U"
        )
        # only applicable to admin_global
        Cru.user_post_fields[permission_type] = _get_fields_with_priv(
            _cru_permissions[permission_type], "C"
        )


_derive_user_priv_fields()
