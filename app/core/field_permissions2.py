"""Variables that define the fields that can be read or updated by a user based on user permissionss

Variables:
    me_endpoint_read_fields: list of fields that can be read by the requesting user for the me endpoint
    me_endpoint_patch_fields: list of fields that can be updated by the requesting user for the me endpoint
    * Note: me_end_point gets or updates information about the requesting user

    user_read_fields: list of fields that can be read by the requesting user for the user endpoint
    user_patch_fields: list of fields that can be updated by the requesting user for the user endpoint
"""

from constants import global_admin
from constants import practice_area_admin
from constants import project_lead
from constants import project_member
from core.user_field_permissions_constants import me_endpoint_permissions
from core.user_field_permissions_constants import self_register_fields
from core.user_field_permissions_constants import user_field_permissions


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


class FieldPermissions2:
    user_read_fields = {
        project_lead: [],
        project_member: [],
        practice_area_admin: [],
        global_admin: [],
    }
    user_patch_fields = {
        project_lead: [],
        project_member: [],
        practice_area_admin: [],
        global_admin: [],
    }
    user_post_fields = {
        project_lead: [],
        project_member: [],
        practice_area_admin: [],
        global_admin: [],
    }
    me_endpoint_read_fields = []
    me_endpoint_patch_fields = []
    self_register_fields = []

    # *************************************************************
    # See pydoc at top of file for description of these variables *
    # *************************************************************

    @classmethod
    def derive_cru_fields(cls):
        cls.me_read_fields = _get_fields_with_priv(me_endpoint_permissions, "R")
        cls.me_patch_fields = _get_fields_with_priv(me_endpoint_permissions, "R")
        cls.self_register_fields = self_register_fields
        for permission_type in [
            project_lead,
            project_member,
            practice_area_admin,
            global_admin,
        ]:
            cls.user_read_fields[permission_type] = _get_fields_with_priv(
                user_field_permissions[permission_type], "R"
            )
            cls.user_patch_fields[permission_type] = _get_fields_with_priv(
                user_field_permissions[permission_type], "U"
            )
            cls.user_post_fields[permission_type] = _get_fields_with_priv(
                user_field_permissions[permission_type], "C"
            )


FieldPermissions2.derive_cru_fields()
