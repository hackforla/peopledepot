from rest_framework.generics import (
    GenericAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated

from ..models import User
from .serializers import UserSerializer


class UserProfileAPIView(RetrieveModelMixin, GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user

    def get(self, request, *args, **kwargs):
        """
        User Profile

        Get prifile of current logged in user.
        """
        return self.retrieve(request, *args, **kwargs)


class UserListCreateAPIView(ListCreateAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    lookup_field = "uuid"


class UserRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    lookup_field = "uuid"
