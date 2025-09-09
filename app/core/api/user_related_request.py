from rest_framework.exceptions import PermissionDenied
from rest_framework.exceptions import ValidationError

from core.api.request_fields_allowed import RequestFieldsAllowed
from core.models import User
from core.models import UserPermission


class UserRelatedRequest:
    """
    Utility class for handling user-related requests, including permissions
    and field validation. Primarily used to filter querysets and validate
    fields based on the requesting user's privileges.
    """

    @staticmethod
    def _get_allowed_users(request):
        """
        Return a queryset of users that the requesting user is allowed to view.

        Admin users can view all users. Non-admin users can only view users
        who share projects that they have permissions for.

        Args:
            request (Request): The DRF request object.

        Returns:
            QuerySet[User]: QuerySet of allowed User objects.
        """
        current_user = User.objects.get(username=request.user.username)
        user_permissions = UserPermission.objects.filter(user=current_user)

        if RequestFieldsAllowed.is_admin(current_user):
            return User.objects.all()

        # Get the projects the user has permissions for
        projects = [p.project for p in user_permissions if p.project is not None]
        return User.objects.filter(permissions__project__in=projects).distinct()

    @classmethod
    def get_queryset(cls, view):
        """
        Get the queryset of objects that the requesting user has permission to view.

        This method is typically called from `get_queryset` in a DRF ViewSet.

        Args:
            view (ViewSet): The DRF view instance.

        Returns:
            QuerySet: The queryset filtered according to the requesting user's permissions.
        """
        allowed_users = cls._get_allowed_users(view.request)
        model_class = view.serializer_class.Meta.model

        if model_class == User:
            return allowed_users
        return model_class.objects.filter(user__in=allowed_users)

    @staticmethod
    def get_serializer_representation(self, instance, original_representation):
        """
        Filter the serializer representation to only include fields
        the requesting user is allowed to see.

        Args:
            instance (Model): The instance being serialized.
            original_representation (dict): The original serializer data.

        Returns:
            dict: A filtered representation containing only permitted fields.
        """
        request = self.context.get("request")
        model_class = self.Meta.model
        response_related_user = instance if model_class == User else instance.user

        # Determine which fields the requesting user can access
        user_fields = RequestFieldsAllowed.get_fields_for_get_request(
            request=request,
            table_name=model_class.__name__,
            response_related_user=response_related_user,
        )

        # Return only allowed fields
        return {
            key: value
            for key, value in original_representation.items()
            if key in user_fields
        }

    @classmethod
    def validate_post_fields(cls, view, request):
        """
        Validate that the fields in a POST request are allowed for the requesting user.

        Args:
            view (ViewSet): The DRF view instance.
            request (Request): The DRF request object.

        Raises:
            PermissionDenied: If the user has no valid fields for the model.
            ValidationError: If the request contains disallowed fields.
        """
        model_class = view.serializer_class.Meta.model
        table_name = model_class.__name__
        valid_fields = RequestFieldsAllowed.get_fields_for_post_request(
            request=request, table_name=table_name
        )
        cls.validate_request_fields(request, valid_fields)

    @classmethod
    def validate_patch_fields(cls, view, request, obj):
        """
        Validate that the fields in a PATCH request are allowed for the requesting user.

        Args:
            view (ViewSet): The DRF view instance.
            request (Request): The DRF request object.
            obj (Model): The instance being patched.

        Raises:
            PermissionDenied: If the user has no valid fields for the model.
            ValidationError: If the request contains disallowed fields.
        """
        model_class = view.serializer_class.Meta.model
        table_name = model_class.__name__
        response_related_user = obj if model_class == User else obj.user
        valid_fields = RequestFieldsAllowed.get_fields_for_patch_request(
            table_name=table_name,
            request=request,
            response_related_user=response_related_user,
        )
        cls.validate_request_fields(request, valid_fields)

    @staticmethod
    def validate_request_fields(request, valid_fields) -> None:
        """
        Ensure the request only contains allowed fields.

        Args:
            request (Request): The DRF request object.
            valid_fields (list[str]): List of fields the user is allowed to modify.

        Raises:
            PermissionDenied: If no fields are valid for this user.
            ValidationError: If the request contains disallowed fields.
        """
        request_keys = set(request.data)
        disallowed_fields = request_keys - set(valid_fields)

        if not valid_fields:
            raise PermissionDenied("You do not have privileges to modify any fields.")
        if disallowed_fields:
            raise ValidationError(f"Invalid fields: {', '.join(disallowed_fields)}")
