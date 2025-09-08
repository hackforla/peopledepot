from rest_framework.permissions import BasePermission

from core.api.user_related_request import UserRelatedRequest


class DenyAny(BasePermission):
    """
    Permission class that denies all requests.

    This class is useful in situations where you want to explicitly
    prevent access to a view or object, regardless of the user or request.
    """

    def has_permission(self, request, view) -> bool:
        """
        Check general permissions for the request.

        Parameters:
            request (Request): The incoming DRF request object.
            view (View): The DRF view being accessed.

        Returns:
            bool: Always returns False, denying all requests.
        """
        return False

    def has_object_permission(self, request, view, obj) -> bool:
        """
        Check object-level permissions for the request.

        Parameters:
            request (Request): The incoming DRF request object.
            view (View): The DRF view being accessed.
            obj (Any): The object being accessed.

        Returns:
            bool: Always returns False, denying all object-level requests.
        """
        return False


class GenericPermission(BasePermission):
    """
    Permission class that allows all requests but performs validation
    for POST and PATCH operations.

    For POST requests, it validates fields using
    `UserRelatedRequest.validate_post_fields`.

    For PATCH requests, it validates fields using
    `UserRelatedRequest.validate_patch_fields`.

    Examples:
        >>> permission = GenericPermission()
        >>> permission.has_permission(request, view)
        True
    """

    def has_permission(self, request, view) -> bool:
        """
        Check general permissions for the request.

        Parameters:
            request (Request): The incoming DRF request object.
            view (View): The DRF view being accessed.

        Returns:
            bool: Always True after running field validation if applicable.
        """
        if request.method == "POST":
            UserRelatedRequest.validate_post_fields(request=request, view=view)
        return True  # Default to allow the request

    def has_object_permission(self, request, view, obj) -> bool:
        """
        Check object-level permissions for the request.

        Parameters:
            request (Request): The incoming DRF request object.
            view (View): The DRF view being accessed.
            obj (Any): The object being accessed.

        Returns:
            bool: Always True after running field validation if applicable.
        """
        if request.method == "PATCH":
            UserRelatedRequest.validate_patch_fields(
                view=view, obj=obj, request=request
            )
        return True
