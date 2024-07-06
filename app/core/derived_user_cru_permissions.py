"""Variables that define the fields that can be read or updated by a user based on user permissionss

Variables:
    me_endpoint_read_fields: list of fields that can be read by the requesting user for the me endpoint
    me_endpoint_update_fields: list of fields that can be updated by the requesting user for the me endpoint
    * Note: me_end_point gets or updates information about the requesting user

    user_read_fields: list of fields that can be read by the requesting user for the user endpoint
    user_update_fields: list of fields that can be updated by the requesting user for the user endpoint
"""

from constants import global_admin
from constants import practice_area_admin
from constants import project_lead
from constants import project_member
from core.base_user_cru_constants import me_endpoint_permissions
from core.base_user_cru_constants import user_field_permissions


# Gets the fields in field_permission that have the permission specified by cru_permission
# Args:
#   field_permissions (dictionary): dictionary of field permissions.  Key: field name. Value: "CRU" or subset.
#   cru_permission (str): permission to check for in field_permissions (C, R, or U)
# Returns:
#   [str]: list of field names that have the specified permission
def _get_fields_with_priv(field_permissions, cru_permission):
    ret_array = []
    for key, value in field_permissions.items():
        if cru_permission in value:
            ret_array.append(key)
    return ret_array


# *************************************************************
# See pydoc at top of file for description of these variables *
# *************************************************************

me_endpoint_read_fields = _get_fields_with_priv(me_endpoint_permissions, "R")
me_endpoint_update_fields = _get_fields_with_priv(me_endpoint_permissions, "U")

user_read_fields = {
    project_lead: _get_fields_with_priv(user_field_permissions[project_lead], "R"),
    project_member: _get_fields_with_priv(user_field_permissions[project_member], "R"),
    practice_area_admin: _get_fields_with_priv(
        user_field_permissions[project_lead], "R"
    ),
    global_admin: _get_fields_with_priv(user_field_permissions[global_admin], "R"),
}

user_update_fields = {
    project_lead: _get_fields_with_priv(user_field_permissions[project_lead], "U"),
    project_member: _get_fields_with_priv(user_field_permissions[project_member], "U"),
    practice_area_admin: _get_fields_with_priv(
        user_field_permissions[project_lead], "U"
    ),
    global_admin: _get_fields_with_priv(user_field_permissions[global_admin], "U"),
}
