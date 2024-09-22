"""
The specified values in these dictionaries are based on the requirements of the project.  They
are in a format to simplify understanding and mapping to the requirements.  The values are used to derive the values
in derived_user_cru_permissions.py.  The application uses the derived values for implementing the
requirements.
"""

from constants import admin_project
from constants import global_admin
from constants import member_project
from constants import practice_lead_project

self_register_fields = [
    "username",
    "first_name",
    "last_name",
    "gmail",
    "preferred_email",
    "linkedin_account",
    "github_handle",
    "phone",
    "texting_ok",
    # "intake_current_job_title",
    # "intake_target_job_title",
    "current_job_title",
    "target_job_title",
    # "intake_current_skills",
    # "intake_target_skills",
    "current_skills",
    "target_skills",
    "time_zone",
    "password",
]


# permissions for the "me" endpoint which is used for the user to view and
# patch their own information
me_endpoint_permissions = {
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
#
user_field_permissions = {
    member_project: {},
    practice_lead_project: {},
    global_admin: {},
}

user_field_permissions[member_project] = {
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

user_field_permissions[practice_lead_project] = {
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

user_field_permissions[admin_project] = user_field_permissions[
    practice_lead_project
].copy()

user_field_permissions[global_admin] = {
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
    "password": "CU",
}
