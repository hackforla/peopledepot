from django.contrib.auth.models import Group
from .helpers import filter_user_queryset
from rest_framework.exceptions import PermissionDenied
from .serializers import UserAppSerializer
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from rest_framework.response import Response

from rest_framework.generics import GenericAPIView
from rest_framework.mixins import RetrieveModelMixin

class UserAppKbViewSet(RetrieveModelMixin, GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserAppSerializer
    lookup_field = "uuid"
    calling_app = "kb" # using variable to make extending to other apps easier

    def get(self, request, **kwargs):
        """
        Optionally filter users by an 'email' and/or 'username' query paramerter in the URL
        """
        user = request.user
        permission_name = f"core.get_api_user_app_{self.calling_app}"
        if not user.has_perm(permission_name):
            raise PermissionDenied(f"You don't have privilege to view users for calling app {self.calling_app}.")
        groups = Group.objects.filter(name__startswith=f"{self.calling_app}_")

        # Filter users who are in any of these groups
        queryset = get_user_model().objects.filter(groups__in=groups).distinct()
        queryset = filter_user_queryset(request, queryset)
        # Serialize the queryset
        serializer = self.get_serializer(queryset, many=True)
        
        # Return a Response object with serialized data
        return Response(serializer.data)

