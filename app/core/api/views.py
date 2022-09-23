from django.contrib.auth import get_user_model
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiParameter,
    extend_schema,
    extend_schema_view,
)
from rest_framework import viewsets
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from ..models import Faq, Project, RecurringEvent
from .permissions import IsOwnerOrReadOnly
from .serializers import (
    FaqSerializer,
    ProjectSerializer,
    RecurringEventSerializer,
    UserSerializer,
)


class UserProfileAPIView(RetrieveModelMixin, GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user

    def get(self, request, *args, **kwargs):
        """
        # User Profile

        Get profile of current logged in user.
        """
        return self.retrieve(request, *args, **kwargs)


@extend_schema_view(
    list=extend_schema(
        summary="Users List",
        description="Return a list of all the existing users",
        parameters=[
            OpenApiParameter(
                name="email",
                type=str,
                description="Filter by email address",
                examples=[
                    OpenApiExample(
                        "Example 1",
                        summary="Test admin email",
                        description="get the test admin user",
                        value="testadmin@email.com,",
                    ),
                ],
            ),
            OpenApiParameter(
                name="username",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="Filter by username",
                examples=[
                    OpenApiExample(
                        "Example 1",
                        summary="Test admin username",
                        description="get the test admin user",
                        value="testadmin",
                    ),
                ],
            ),
        ],
    ),
    create=extend_schema(description="Create a new user"),
    retrieve=extend_schema(description="Return the given user"),
    destroy=extend_schema(description="Delete the given user"),
    update=extend_schema(description="Update the given user"),
    partial_update=extend_schema(description="Partially update the given user"),
)
class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == "create":
            permission_classes = [
                IsAdminUser,
            ]
        else:
            permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        """
        Optionally filter users by an 'email' query paramerter in the URL
        """
        queryset = get_user_model().objects.all()
        email = self.request.query_params.get("email")
        if email is not None:
            queryset = queryset.filter(email=email)
        username = self.request.query_params.get("username")
        if username is not None:
            queryset = queryset.filter(username=username)
        return queryset


@extend_schema_view(
    list=extend_schema(
        summary="Projects List",
        description="Return a list of all the existing projects",
    ),
)
class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def get_permissions(self):
        if self.action == "create":
            permission_classes = [
                IsAdminUser,
            ]
        else:
            permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
        return [permission() for permission in permission_classes]


@extend_schema_view(
    list=extend_schema(
        summary="Recurring Events",
        description="Return a list of all the existing recurring events",
    ),
)
class RecurringEventViewSet(viewsets.ModelViewSet):
    queryset = RecurringEvent.objects.all()
    serializer_class = RecurringEventSerializer

    def get_permissions(self):
        if self.action == "create":
            permission_classes = [
                IsAdminUser,
            ]
        else:
            permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
        return [permission() for permission in permission_classes]


class FaqViewSet(viewsets.ModelViewSet):
    queryset = Faq.objects.all()
    serializer_class = FaqSerializer
    # use permission_classes until get_permissions fn provides sufficient limits to access >>
    permission_classes = [IsAuthenticated]
