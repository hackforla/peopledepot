from django.contrib.auth.models import Group
from .helpers import filter_user_queryset
from .serializers import UserAppSerializer
from .permissions import UserAppKbPermission
from django.contrib.auth import get_user_model
from rest_framework.response import Response

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .helpers import filter_user_queryset
from .permissions import UserAppKbPermission
from .serializers import UserAppSerializer


class UserAppKbApiView(RetrieveModelMixin, GenericAPIView):
    permission_classes = [UserAppKbPermission]
    serializer_class = UserAppSerializer
    lookup_field = "uuid"
    calling_app = "kb"  # using variable to make extending to other apps easier

    def get(self, request, **kwargs):
        """
        Optionally filter users by an 'email' and/or 'username' query paramerter in the URL
        """
        groups = Group.objects.filter(name__startswith=f"{self.calling_app}_")
        queryset = get_user_model().objects.filter(groups__in=groups).distinct()
        queryset = filter_user_queryset(request, queryset)
        # Serialize the queryset
        serializer = self.get_serializer(queryset, many=True)

        # Return a Response object with serialized data
        return Response(serializer.data)
