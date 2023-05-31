from django.contrib.auth import get_user_model
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiExample
from drf_spectacular.utils import OpenApiParameter
from drf_spectacular.utils import extend_schema
from drf_spectacular.utils import extend_schema_view
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from ..models import Faq
from ..models import FaqViewed
from ..models import Location
from ..models import PracticeArea
from ..models import Project
from ..models import RecurringEvent
from ..models import SponsorPartner
from .serializers import FaqSerializer
from .serializers import FaqViewedSerializer
from .serializers import LocationSerializer
from .serializers import PracticeAreaSerializer
from .serializers import ProjectSerializer
from .serializers import RecurringEventSerializer
from .serializers import SponsorPartnerSerializer
from .serializers import UserSerializer


class UserProfileAPIView(RetrieveModelMixin, GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

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
                        summary="Demo email",
                        description="get the demo user",
                        value="demo-email@email.com,",
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
                        summary="Demo username",
                        description="get the demo user",
                        value="demo-user",
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
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    lookup_field = "uuid"

    def get_queryset(self):
        """
        Optionally filter users by an 'email' and/or 'username' query paramerter in the URL
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
    list=extend_schema(description="Return a list of all the projects"),
    create=extend_schema(description="Create a new project"),
    retrieve=extend_schema(description="Return the details of a project"),
    destroy=extend_schema(description="Delete a project"),
    update=extend_schema(description="Update a project"),
    partial_update=extend_schema(description="Patch a project"),
)
class ProjectViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


@extend_schema_view(
    list=extend_schema(description="Return a list of all the recurring events"),
    create=extend_schema(description="Create a new recurring event"),
    retrieve=extend_schema(description="Return the details of a recurring event"),
    destroy=extend_schema(description="Delete a recurring event"),
    update=extend_schema(description="Update a recurring event"),
    partial_update=extend_schema(description="Patch a recurring event"),
)
class RecurringEventViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = RecurringEvent.objects.all()
    serializer_class = RecurringEventSerializer


@extend_schema_view(
    list=extend_schema(description="Return a list of all the practice areas"),
    create=extend_schema(description="Create a new sponsor practice area"),
    retrieve=extend_schema(description="Return the details of a practice area"),
    destroy=extend_schema(description="Delete a practice area"),
    update=extend_schema(description="Update a practice area"),
    partial_update=extend_schema(
        description="Patch (partially update) a practice area"
    ),
)
class PracticeAreaViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = PracticeArea.objects.all()
    serializer_class = PracticeAreaSerializer


@extend_schema_view(
    list=extend_schema(description="Return a list of all the sponsor partners"),
    create=extend_schema(description="Create a new sponsor partner"),
    retrieve=extend_schema(description="Return the details of a sponsor partner"),
    destroy=extend_schema(description="Delete a sponsor partner"),
    update=extend_schema(description="Update a sponsor partner"),
    partial_update=extend_schema(description="Patch a sponsor partner"),
)
class SponsorPartnerViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = SponsorPartner.objects.all()
    serializer_class = SponsorPartnerSerializer

    # The following code can be uncommented and used later, but it's being left out
    # for simplicity's sake during initial model creation
    #
    # def get_queryset(self):
    #     """
    #     Optionally filter sponsor partners by name, is_active, and/or is_sponsor query parameters in the URL
    #     """
    #     queryset = SponsorPartner.objects.all()
    #     partner_name = self.request.query_params.get("partner_name")
    #     if partner_name is not None:
    #         queryset = queryset.filter(partner_name=partner_name)
    #     is_active = self.request.query_params.get("is_active")
    #     if is_active is not None:
    #         queryset = queryset.filter(is_active=is_active)
    #     is_sponsor = self.request.query_params.get("is_sponsor")
    #     if is_sponsor is not None:
    #         queryset = queryset.filter(is_sponsor=is_sponsor)
    #     return queryset


@extend_schema_view(
    list=extend_schema(description="Return a list of all FAQs"),
    create=extend_schema(description="Create a new FAQ"),
    retrieve=extend_schema(description="Return the given FAQ"),
    destroy=extend_schema(description="Delete the given FAQ"),
    update=extend_schema(description="Update the given FAQ"),
    partial_update=extend_schema(description="Partially update the given FAQ"),
)
class FaqViewSet(viewsets.ModelViewSet):
    queryset = Faq.objects.all()
    serializer_class = FaqSerializer
    # use permission_classes until get_permissions fn provides sufficient limits to access >>
    permission_classes = [IsAuthenticated]


@extend_schema_view(
    list=extend_schema(description="Return a list of all FAQs viewed"),
    create=extend_schema(description="Create a new FAQ viewed"),
    retrieve=extend_schema(description="Return the given FAQ viewed"),
)
class FaqViewedViewSet(mixins.CreateModelMixin, viewsets.ReadOnlyModelViewSet):
    queryset = FaqViewed.objects.all()
    serializer_class = FaqViewedSerializer
    permission_classes = [IsAuthenticated]


@extend_schema_view(
    list=extend_schema(description="Return a list of all locations"),
    create=extend_schema(description="Create a new location"),
    retrieve=extend_schema(description="Return the details of a location"),
    destroy=extend_schema(description="Delete a location"),
    update=extend_schema(description="Update a location"),
    partial_update=extend_schema(description="Patch a location"),
)
class LocationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
