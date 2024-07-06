from constants import global_admin
from constants import practice_area_admin
from constants import project_lead
from constants import project_member
from core.base_user_cru_constants import me_endpoint_permissions
from core.base_user_cru_constants import user_field_permissions


def _get_fields(field_privs, crud_priv):
    ret_array = []
    for key, value in field_privs.items():
        if crud_priv in value:
            ret_array.append(key)
    return ret_array


me_endpoint_read_fields = _get_fields(me_endpoint_permissions, "R")
me_endpoint_update_fields = _get_fields(me_endpoint_permissions, "U")

user_read_fields = {
    project_lead: _get_fields(user_field_permissions[project_lead], "R"),
    project_member: _get_fields(user_field_permissions[project_member], "R"),
    practice_area_admin: _get_fields(user_field_permissions[project_lead], "R"),
    global_admin: _get_fields(user_field_permissions[global_admin], "R"),
}

user_update_fields = {
    project_lead: _get_fields(user_field_permissions[project_lead], "U"),
    project_member: _get_fields(user_field_permissions[project_member], "U"),
    practice_area_admin: _get_fields(user_field_permissions[project_lead], "U"),
    global_admin: _get_fields(user_field_permissions[global_admin], "U"),
}
