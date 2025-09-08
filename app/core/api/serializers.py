from rest_framework import serializers
from timezone_field.rest_framework import TimeZoneSerializerField

from core.api.user_related_request import UserRelatedRequest
from core.models import Affiliate
from core.models import Affiliation
from core.models import CheckType
from core.models import Event
from core.models import EventType
from core.models import Faq
from core.models import FaqViewed
from core.models import LeadershipType
from core.models import Location
from core.models import PermissionType
from core.models import PracticeArea
from core.models import ProgramArea
from core.models import Project
from core.models import ProjectStatus
from core.models import Referrer
from core.models import ReferrerType
from core.models import Sdg
from core.models import Skill
from core.models import SocMajor
from core.models import StackElement
from core.models import StackElementType
from core.models import UrlType
from core.models import User
from core.models import UserPermission
from core.models import UserStatusType

# ------------------------
# Base serializers
# ------------------------


class ReadOnlyBaseSerializer(serializers.ModelSerializer):
    """Base serializer with common read-only fields."""

    class Meta:
        abstract = True
        read_only_fields = ("uuid", "created_at", "updated_at")


class BaseUserSerializer(ReadOnlyBaseSerializer):
    """
    Base serializer for the User model.

    Includes all commonly needed fields when retrieving user info.
    Intended to be inherited by other serializers to avoid repetition.

    Attributes:
        time_zone: Uses TimeZoneSerializerField (without pytz) for user time zones.
    """

    time_zone = TimeZoneSerializerField(use_pytz=False)

    class Meta(ReadOnlyBaseSerializer.Meta):
        model = User
        fields = (
            "uuid",
            "username",
            "created_at",
            "updated_at",
            "is_superuser",
            "is_active",
            "is_staff",
            "email",
            "first_name",
            "last_name",
            "email_gmail",
            "email_preferred",
            "job_title_current_intake",
            "job_title_target_intake",
            "current_skills",
            "target_skills",
            "referrer",
            "linkedin_account",
            "github_handle",
            "slack_id",
            "phone",
            "texting_ok",
            "time_zone",
            "practice_area_primary",
            "practice_area_secondary",
            "practice_area_target_intake",
            "email_cognito",
            "user_status",
        )


class UserSerializer(BaseUserSerializer):
    """
    Serializer for retrieving full user info with custom representation.

    Overrides `to_representation` to include computed or related fields via
    UserRelatedRequest.get_serializer_representation.
    """

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return UserRelatedRequest.get_serializer_representation(
            self, instance, representation
        )


class UserProfileSerializer(BaseUserSerializer):
    """
    Serializer for retrieving basic user profile information.

    Inherits from BaseUserSerializer without modifying to_representation.
    Use for endpoints where standard model fields suffice.
    """

    pass


# ------------------------
# Other serializers
# ------------------------


class PracticeAreaSerializer(ReadOnlyBaseSerializer):
    """Retrieve practice area info."""

    class Meta(ReadOnlyBaseSerializer.Meta):
        model = PracticeArea
        fields = ("uuid", "created_at", "updated_at", "name", "description")


class UserPermissionSerializer(ReadOnlyBaseSerializer):
    """Retrieve user permission info."""

    class Meta(ReadOnlyBaseSerializer.Meta):
        model = UserPermission
        fields = (
            "uuid",
            "created_at",
            "updated_at",
            "user",
            "permission_type",
            "project",
            "practice_area",
        )


class ProjectSerializer(ReadOnlyBaseSerializer):
    """Retrieve project info."""

    sdgs = serializers.StringRelatedField(many=True)  # read-only
    program_areas = serializers.StringRelatedField(many=True)  # read-only

    class Meta(ReadOnlyBaseSerializer.Meta):
        model = Project
        fields = (
            "uuid",
            "name",
            "description",
            "created_at",
            "updated_at",
            "completed_at",
            "github_org_id",
            "github_primary_repo_id",
            "hide",
            "leadership_type",
            "google_drive_id",
            "image_logo",
            "image_hero",
            "image_icon",
            "sdgs",
            "program_areas",
        )


class EventSerializer(ReadOnlyBaseSerializer):
    """Retrieve event info."""

    class Meta(ReadOnlyBaseSerializer.Meta):
        model = Event
        fields = (
            "uuid",
            "name",
            "start_time",
            "duration_in_min",
            "video_conference_url",
            "additional_info",
            "project",
        )


class EventTypeSerializer(ReadOnlyBaseSerializer):
    """Retrieve event type info."""

    class Meta(ReadOnlyBaseSerializer.Meta):
        model = EventType
        fields = ("uuid", "name", "description")


class AffiliateSerializer(ReadOnlyBaseSerializer):
    """Retrieve sponsor/partner info."""

    class Meta(ReadOnlyBaseSerializer.Meta):
        model = Affiliate
        fields = (
            "uuid",
            "partner_name",
            "partner_logo",
            "is_active",
            "url",
            "is_org_sponsor",
            "is_org_partner",
        )


class FaqSerializer(ReadOnlyBaseSerializer):
    """Retrieve FAQ info."""

    class Meta(ReadOnlyBaseSerializer.Meta):
        model = Faq
        fields = ("uuid", "question", "answer", "tool_tip_name")
        read_only_fields = ReadOnlyBaseSerializer.Meta.read_only_fields + (
            "created_on",
            "last_updated",
        )


class FaqViewedSerializer(ReadOnlyBaseSerializer):
    """Retrieve FAQ view info."""

    class Meta(ReadOnlyBaseSerializer.Meta):
        model = FaqViewed
        fields = ("uuid", "faq")
        read_only_fields = ("uuid", "faq")


class LeadershipTypeSerializer(ReadOnlyBaseSerializer):
    """Retrieve leadership type info."""

    class Meta(ReadOnlyBaseSerializer.Meta):
        model = LeadershipType
        fields = ("uuid", "name", "description")


class LocationSerializer(ReadOnlyBaseSerializer):
    """Retrieve location info."""

    zip = serializers.CharField(source="zipcode")

    class Meta(ReadOnlyBaseSerializer.Meta):
        model = Location
        fields = (
            "uuid",
            "name",
            "address_line_1",
            "address_line_2",
            "city",
            "state",
            "zip",
            "phone",
        )


class ProgramAreaSerializer(ReadOnlyBaseSerializer):
    """Retrieve program area info."""

    projects = serializers.StringRelatedField(many=True)  # read-only

    class Meta(ReadOnlyBaseSerializer.Meta):
        model = ProgramArea
        fields = ("uuid", "name", "description", "image", "projects")


class SkillSerializer(ReadOnlyBaseSerializer):
    """Retrieve skill info."""

    class Meta(ReadOnlyBaseSerializer.Meta):
        model = Skill
        fields = ("uuid", "name")


class StackElementSerializer(ReadOnlyBaseSerializer):
    """Retrieve stack element info."""

    class Meta(ReadOnlyBaseSerializer.Meta):
        model = StackElement
        fields = (
            "uuid",
            "name",
            "description",
            "url",
            "logo",
            "active",
            "element_type",
        )


class PermissionTypeSerializer(ReadOnlyBaseSerializer):
    """Retrieve permission type info."""

    class Meta(ReadOnlyBaseSerializer.Meta):
        model = PermissionType
        fields = ("uuid", "name", "description")


class StackElementTypeSerializer(ReadOnlyBaseSerializer):
    """Retrieve stack element type info."""

    class Meta(ReadOnlyBaseSerializer.Meta):
        model = StackElementType
        fields = ("uuid", "name", "description")


class SdgSerializer(ReadOnlyBaseSerializer):
    """Retrieve SDG info."""

    projects = serializers.StringRelatedField(many=True)  # read-only

    class Meta(ReadOnlyBaseSerializer.Meta):
        model = Sdg
        fields = ("uuid", "name", "description", "image", "projects")


class AffiliationSerializer(ReadOnlyBaseSerializer):
    """Retrieve affiliation info."""

    class Meta(ReadOnlyBaseSerializer.Meta):
        model = Affiliation
        fields = (
            "uuid",
            "affiliate",
            "project",
            "created_at",
            "ended_at",
            "is_sponsor",
            "is_partner",
        )


class CheckTypeSerializer(ReadOnlyBaseSerializer):
    """Retrieve check type info."""

    class Meta(ReadOnlyBaseSerializer.Meta):
        model = CheckType
        fields = ("uuid", "name", "description")


class ProjectStatusSerializer(ReadOnlyBaseSerializer):
    """Retrieve project status info."""

    class Meta(ReadOnlyBaseSerializer.Meta):
        model = ProjectStatus
        fields = ("uuid", "name", "description")


class SocMajorSerializer(ReadOnlyBaseSerializer):
    """Retrieve SOC major info."""

    class Meta(ReadOnlyBaseSerializer.Meta):
        model = SocMajor
        fields = ("uuid", "occ_code", "title")


class UrlTypeSerializer(ReadOnlyBaseSerializer):
    """Retrieve URL type info."""

    class Meta(ReadOnlyBaseSerializer.Meta):
        model = UrlType
        fields = ("uuid", "name", "description")


class UserStatusTypeSerializer(ReadOnlyBaseSerializer):
    """Retrieve user status type info."""

    class Meta(ReadOnlyBaseSerializer.Meta):
        model = UserStatusType
        fields = ("uuid", "name", "description")


class ReferrerTypeSerializer(ReadOnlyBaseSerializer):
    """Retrieve referrer type info."""

    class Meta(ReadOnlyBaseSerializer.Meta):
        model = ReferrerType
        fields = ("uuid", "name", "description")


class ReferrerSerializer(ReadOnlyBaseSerializer):
    """Retrieve referrer info."""

    class Meta(ReadOnlyBaseSerializer.Meta):
        model = Referrer
        fields = (
            "uuid",
            "name",
            "url",
            "referrer_type",
            "contact_name",
            "contact_email",
        )
