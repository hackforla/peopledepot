from django.contrib.auth import get_user_model
from rest_framework.generics import (
    GenericAPIView,
)
from rest_framework import viewsets
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


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
