from django.contrib.auth import get_user_model
from rest_framework.exceptions import PermissionDenied
from rest_framework.exceptions import ValidationError

from core.models import User
from core.models import UserPermission

from .access_control import AccessControl


class UserRelatedRequest:
    @staticmethod
    def get_permitted_users(request):
        current_username = request.user.username

        current_user = get_user_model().objects.get(username=current_username)
        user_permissions = UserPermission.objects.filter(user=current_user)

        if AccessControl.is_admin(current_user):
            permitted_users = get_user_model().objects.all()
        else:
            # Get the users with user permissions for the same projects
            # that the requesting_user has permission to view
            projects = [p.project for p in user_permissions if p.project is not None]
            permitted_users = (
                get_user_model()
                .objects.filter(permissions__project__in=projects)
                .distinct()
            )
        return permitted_users

    @classmethod
    def get_queryset(cls, view):
        """Get the queryset of users that the requesting user has permission to view.

        Called from get_queryset in UserViewSet in views.py.

        Args:
            request: the request object

        Returns:
            queryset: the queryset of users that the requesting user has permission to view
        """
        permitted_users = cls.get_permitted_users(view.request)
        current_model = view.serializer_class.Meta.model
        if current_model == User:
            queryset = permitted_users
        else:
            queryset = current_model.objects.filter(user__in=permitted_users)

        return queryset

    @staticmethod
    def get_serializer_representation(self, instance, original_representation):
        request = self.context.get("request")
        model_class = self.Meta.model
        if model_class == User:
            response_related_user: User = instance
        else:
            response_related_user = instance.user
        # Get dynamic fields from some logic
        user_fields = AccessControl.get_response_fields(
            request=request,
            table_name=model_class.__name__,
            response_related_user=response_related_user,
        )
        # Only retain the fields you want to include in the output
        return {
            key: value
            for key, value in original_representation.items()
            if key in user_fields
        }

    @classmethod
    def validate_post_fields(cls, view, request):
        # todo
        serializer_class = view.serializer_class
        table_name = serializer_class.Meta.model.__name__
        valid_fields = AccessControl.get_fields_for_post_request(
            request=request, table_name=table_name
        )
        cls._validate_request_fields(request, valid_fields)

    @classmethod
    def validate_patch_fields(cls, view, request, obj):
        serializer_class = view.serializer_class
        model_class = serializer_class.Meta.model
        table_name = model_class.__name__
        if model_class == User:
            response_related_user = obj
        else:
            response_related_user = obj.user
        valid_fields = AccessControl.get_fields_for_patch_request(
            table_name=table_name,
            request=request,
            response_related_user=response_related_user,
        )
        cls._validate_request_fields(request, valid_fields)

    @staticmethod
    def _validate_request_fields(request, valid_fields) -> None:
        """Ensure the requesting user can patch the provided fields."""
        request_data_keys = set(request.data)
        notpermitted_fields = request_data_keys - set(valid_fields)
        if not valid_fields:
            raise PermissionDenied("You do not have privileges ")
        elif notpermitted_fields:
            raise ValidationError(f"Invalid fields: {', '.join(notpermitted_fields)}")
