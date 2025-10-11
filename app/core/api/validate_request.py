from core.models import User
from.access_control import AccessControl
from rest_framework.exceptions import PermissionDenied, ValidationError

def validate_post_fields(view, request):
    # todo
    serializer_class = view.serializer_class
    table_name = serializer_class.Meta.model.__name__
    permitted_fields = _get_permitted_fields_for_post_request(
        request=request, table_name=table_name
    )
    _validate_request_fields_permitted(request, permitted_fields)


def get_fields_for_patch_request(request, table_name, response_related_user):
    requesting_user = request.user
    requesting_user = request.user
    most_privileged_perm_type = (
        AccessControl.get_highest_shared_project_perm_type(
            requesting_user, response_related_user
        )
    )
    fields = AccessControl.get_permitted_fields(
        operation="patch",
        table_name=table_name,
        permission_type=most_privileged_perm_type,
    )
    return fields


def _get_permitted_fields_for_post_request(request, table_name):
    highest_perm_type = AccessControl.get_highest_user_perm_type(request.user)
    fields = AccessControl.get_permitted_fields(
        operation="post",
        table_name=table_name,
        permission_type=highest_perm_type,
    )
    return fields


def _get_related_user_from_obj(obj):
    if hasattr(obj, "user"):
        return obj.user
    elif isinstance(obj, User):
        return obj
    else:
        raise ValueError("Cannot determine related user from the given object.")


def validate_patch_fields(request, obj):
    table_name = obj.__class__.__name__
    response_related_user = _get_related_user_from_obj(obj)
    valid_fields = get_fields_for_patch_request(
        table_name=table_name,
        request=request,
        response_related_user=response_related_user,
    )
    _validate_request_fields_permitted(request, valid_fields)

# @staticmethod
def _validate_request_fields_permitted(request, valid_fields) -> None:
    """Ensure the requesting user can patch the provided fields."""
    request_fields_set = set(request.data)
    permitted_fields_set = set(valid_fields)
    notpermitted_fields = request_fields_set - permitted_fields_set
    if not permitted_fields_set:
        raise PermissionDenied("You do not have privileges ")
    elif notpermitted_fields:
        raise ValidationError(f"Invalid fields: {', '.join(notpermitted_fields)}")
