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

from core.permission_util import PermissionUtil

from ..models import Affiliate
from ..models import Affiliation
from ..models import CheckType
from ..models import Event
from ..models import Faq
from ..models import FaqViewed
from ..models import Location
from ..models import PermissionType
from ..models import PracticeArea
from ..models import ProgramArea
from ..models import Project
from ..models import Sdg
from ..models import Skill
from ..models import SocMajor
from ..models import StackElement
from ..models import StackElementType
from ..models import UserPermission
from .serializers import AffiliateSerializer
from .serializers import AffiliationSerializer
from .serializers import CheckTypeSerializer
from .serializers import EventSerializer
from .serializers import FaqSerializer
from .serializers import FaqViewedSerializer
from .serializers import LocationSerializer
from .serializers import PermissionTypeSerializer
from .serializers import PracticeAreaSerializer
from .serializers import ProfileSerializer
from .serializers import ProgramAreaSerializer
from .serializers import ProjectSerializer
from .serializers import SdgSerializer
from .serializers import SkillSerializer
from .serializers import SocMajorSerializer
from .serializers import StackElementSerializer
from .serializers import StackElementTypeSerializer
from .serializers import UserPermissionSerializer
from .serializers import UserSerializer


@extend_schema_view(
    list=extend_schema(
        summary="Your Profile",
        description="Return your profile information",
        parameters=[],
    ),
    retrieve=extend_schema(description="Fetch your user profile"),
    partial_update=extend_schema(description="Update your profile"),
)
class UserProfileAPIView(RetrieveModelMixin, GenericAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "partial_update"]

    def get_object(self):
        """Returns the user profile fetched by get

        Returns:
            User: The user profile
        """

        return self.request.user

    def get(self, request, *args, **kwargs):
        """
        # User Profile

        Get profile for current logged in user.

        Returns:
          User: The user profile
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
    update=extend_schema(description="Update the given user"),
    partial_update=extend_schema(description="Update the given user"),
)
class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    lookup_field = "uuid"

    def get_queryset(self):
        """
        Optionally filter users by an 'email' and/or 'username' query paramerter in the URL
        """
        queryset = PermissionUtil.get_user_queryset(self.request)

        email = self.request.query_params.get("email")
        if email is not None:
            queryset = queryset.filter(email=email)
        username = self.request.query_params.get("username")
        if username is not None:
            queryset = queryset.filter(username=username)
        return queryset

    def create(self, request, *args, **kwargs):
        # Get the parameters for the update
        new_user_data = request.data
        if "time_zone" not in new_user_data:
            new_user_data["time_zone"] = "America/Los_Angeles"

        # Log or print the instance and update_data for debugging
        PermissionUtil.validate_fields_postable(request.user, new_user_data)
        response = super().create(request, *args, **kwargs)
        return response

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()

        # Get the parameters for the update
        update_data = request.data

        # Log or print the instance and update_data for debugging
        PermissionUtil.validate_fields_patchable(request.user, instance, update_data)
        response = super().partial_update(request, *args, **kwargs)
        return response


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
    list=extend_schema(description="Return a list of all the events"),
    create=extend_schema(description="Create a new event"),
    retrieve=extend_schema(description="Return the details of an event"),
    destroy=extend_schema(description="Delete an event"),
    update=extend_schema(description="Update an event"),
    partial_update=extend_schema(description="Patch an event"),
)
class EventViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Event.objects.all()
    serializer_class = EventSerializer


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
    list=extend_schema(description="Return a list of all the affiliates"),
    create=extend_schema(description="Create a new affiliate"),
    retrieve=extend_schema(description="Return the details of a affiliate"),
    destroy=extend_schema(description="Delete a affiliate"),
    update=extend_schema(description="Update a affiliate"),
    partial_update=extend_schema(description="Patch a affiliate"),
)
class AffiliateViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Affiliate.objects.all()
    serializer_class = AffiliateSerializer

    # The following code can be uncommented and used later, but it's being left out
    # for simplicity's sake during initial model creation
    #
    # def get_queryset(self):
    #     """
    #     Optionally filter sponsor partners by name, is_active, and/or is_sponsor query parameters in the URL
    #     """
    #     queryset = Affiliate.objects.all()
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
    partial_update=extend_schema(description="Partially patch the given FAQ"),
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


@extend_schema_view(
    list=extend_schema(description="Return a list of all the program areas"),
    create=extend_schema(description="Create a new program area"),
    retrieve=extend_schema(description="Return the details of a program area"),
    destroy=extend_schema(description="Delete a program area"),
    update=extend_schema(description="Update a program area"),
    partial_update=extend_schema(description="Patch a program area"),
)
class ProgramAreaViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = ProgramArea.objects.all()
    serializer_class = ProgramAreaSerializer


@extend_schema_view(
    list=extend_schema(description="Return a list of all skills"),
    create=extend_schema(description="Create a new skill"),
    retrieve=extend_schema(description="Return the details of a skill"),
    destroy=extend_schema(description="Delete a skill"),
    update=extend_schema(description="Update a skill"),
    partial_update=extend_schema(description="Patch a skill"),
)
class SkillViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer


@extend_schema_view(
    list=extend_schema(description="Return a list of all the stack elements"),
    create=extend_schema(description="Create a new stack element"),
    retrieve=extend_schema(description="Return the details of a stack element"),
    destroy=extend_schema(description="Delete a stack element"),
    update=extend_schema(description="Update a stack element"),
    partial_update=extend_schema(description="Patch a stack element"),
)
class StackElementViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = StackElement.objects.all()
    serializer_class = StackElementSerializer


@extend_schema_view(
    list=extend_schema(description="Return a list of all permission types"),
    create=extend_schema(description="Create a new permission type"),
    retrieve=extend_schema(description="Return the details of a permission type"),
    destroy=extend_schema(description="Delete a permission type"),
    update=extend_schema(description="Update a permission type"),
    partial_update=extend_schema(description="Patch a permission type"),
)
class PermissionTypeViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = PermissionType.objects.all()
    serializer_class = PermissionTypeSerializer


@extend_schema_view(
    list=extend_schema(description="Return a list of all the stack element types"),
    create=extend_schema(description="Create a new stack element type"),
    retrieve=extend_schema(description="Return the details stack element type"),
    destroy=extend_schema(description="Delete a stack element type"),
    update=extend_schema(description="Update a stack element type"),
    partial_update=extend_schema(description="Patch a stack element type"),
)
class StackElementTypeViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = StackElementType.objects.all()
    serializer_class = StackElementTypeSerializer


@extend_schema_view(
    list=extend_schema(description="Return a list of all the recurring events"),
    create=extend_schema(description="Create a new recurring event"),
    retrieve=extend_schema(description="Return the details of a recurring event"),
    destroy=extend_schema(description="Delete a recurring event"),
    update=extend_schema(description="Update a recurring event"),
    partial_update=extend_schema(description="Patch a recurring event"),
)
class SdgViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Sdg.objects.all()
    serializer_class = SdgSerializer


@extend_schema_view(
    list=extend_schema(description="Return a list of all the affiliations"),
    create=extend_schema(description="Create a new affiliation"),
    retrieve=extend_schema(description="Return the details of an affiliation"),
    destroy=extend_schema(description="Delete an affiliation"),
    update=extend_schema(description="Update an affiliation"),
    partial_update=extend_schema(description="Patch an affiliation"),
)
class AffiliationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Affiliation.objects.all()
    serializer_class = AffiliationSerializer


@extend_schema_view(
    list=extend_schema(description="Return a list of all the check_type"),
    create=extend_schema(description="Create a new check_type"),
    retrieve=extend_schema(description="Return the details of an check_type"),
    destroy=extend_schema(description="Delete an check_type"),
    update=extend_schema(description="Update an check_type"),
    partial_update=extend_schema(description="Patch an check_type"),
)
class CheckTypeViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = CheckType.objects.all()
    serializer_class = CheckTypeSerializer


@extend_schema_view(
    list=extend_schema(description="Return a list of all the user permissions"),
    retrieve=extend_schema(description="Return the details of a user permission"),
)
class UserPermissionViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = []
    queryset = UserPermission.objects.all()
    serializer_class = UserPermissionSerializer


@extend_schema_view(
    list=extend_schema(description="Return a list of all the soc majors"),
    create=extend_schema(description="Create a new soc major"),
    retrieve=extend_schema(description="Return the details of a soc major"),
    destroy=extend_schema(description="Delete a soc major"),
    update=extend_schema(description="Update a soc major"),
    partial_update=extend_schema(description="Patch a soc major"),
)
class SocMajorViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = SocMajor.objects.all()
    serializer_class = SocMajorSerializer
