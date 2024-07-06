from constants import global_admin
from constants import practice_area_admin
from constants import project_lead
from constants import project_member
from constants import self_value
from core.user_cru_constants import user_field_permissions


def _get_fields(field_privs, crud_priv):
    ret_array = []
    for key, value in field_privs.items():
        if crud_priv in value:
            ret_array.append(key)
    return ret_array


class UserCruPermissions:
    read_fields = {
        self_value: _get_fields(user_field_permissions[self_value], "R"),
        project_lead: _get_fields(user_field_permissions[project_lead], "R"),
        project_member: _get_fields(user_field_permissions[project_member], "R"),
        practice_area_admin: _get_fields(user_field_permissions[project_lead], "R"),
        global_admin: _get_fields(user_field_permissions[global_admin], "R"),
    }

    update_fields = {
        self_value: _get_fields(user_field_permissions[self_value], "U"),
        project_lead: _get_fields(user_field_permissions[project_lead], "U"),
        project_member: _get_fields(user_field_permissions[project_member], "U"),
        practice_area_admin: _get_fields(user_field_permissions[project_lead], "U"),
        global_admin: _get_fields(user_field_permissions[global_admin], "U"),
    }
