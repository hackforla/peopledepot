from rest_framework.exceptions import (
    ValidationError,
    PermissionDenied,
    MethodNotAllowed,
)

from core.models import User
from core.models import UserPermission
from core.api.permission_validation import PermissionValidation



class UserRequest:
    @staticmethod
    def get_queryset(request):
        """Get the queryset of users that the requesting user has permission to view.

        Called from get_queryset in UserViewSet in views.py.

        Args:
            request: the request object

        Returns:
            queryset: the queryset of users that the requesting user has permission to view
        """
        current_username = request.user.username

        current_user = User.objects.get(username=current_username)
        user_permissions = UserPermission.objects.filter(user=current_user)

        if PermissionValidation.is_admin(current_user):
            queryset = User.objects.all()
        else:
            # Get the users with user permissions for the same projects
            # that the requester has permission to view
            projects = [p.project for p in user_permissions if p.project is not None]
            queryset = User.objects.filter(permissions__project__in=projects).distinct()
        return queryset

    @staticmethod
    def validate_fields(request, target_user=None) -> None:
        """Ensure the requesting user can patch the provided fields."""
        valid_fields = []
        if request.method == "POST":
            valid_fields = PermissionValidation.get_fields_for_post_request(
                request=request, table_name="user"
            )
        elif request.method == "PATCH":
            valid_fields = PermissionValidation.get_fields_for_request(
                table_name="user",
                request=request,
                operation="patch",
                target_user=target_user,
            )
        else:
            raise MethodNotAllowed("Not valid for REST method", request.method)
        request_data_keys = set(request.data)
        disallowed_fields = request_data_keys - set(valid_fields)

        if not valid_fields:
            raise PermissionDenied(f"You do not have privileges ")
        elif disallowed_fields:
            raise ValidationError(f"Invalid fields: {', '.join(disallowed_fields)}")

