from rest_framework import serializers
from timezone_field.rest_framework import TimeZoneSerializerField

from core.api.cru import Cru
from core.api.cru import profile_value
from core.api.permission_check import PermissionCheck
from core.models import Affiliate
from core.models import Affiliation
from core.models import CheckType
from core.models import Event
from core.models import Faq
from core.models import FaqViewed
from core.models import Location
from core.models import PermissionType
from core.models import PracticeArea
from core.models import ProgramArea
from core.models import Project
from core.models import Sdg
from core.models import Skill
from core.models import SocMajor
from core.models import StackElement
from core.models import StackElementType
from core.models import User
from core.models import UserPermission


class PracticeAreaSerializer(serializers.ModelSerializer):
    """Used to retrieve practice area info"""

    class Meta:
        model = PracticeArea
        fields = (
            "uuid",
            "created_at",
            "updated_at",
            "name",
            "description",
        )
        read_only_fields = (
            "uuid",
            "created_at",
            "updated_at",
        )


class UserPermissionSerializer(serializers.ModelSerializer):
    """Used to retrieve user permissions"""

    class Meta:
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
        read_only_fields = (
            "uuid",
            "created_at",
            "updated_at",
        )


class UserSerializer(serializers.ModelSerializer):
    """Used to retrieve user info"""

    time_zone = TimeZoneSerializerField(use_pytz=False)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request_user: User = self.context["request"].user
        # Get dynamic fields from some logic
        user_fields = PermissionCheck.get_user_read_fields(request_user, instance)
        # Only retain the fields you want to include in the output
        return {
            key: value for key, value in representation.items() if key in user_fields
        }

    class Meta:
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
            "gmail",
            "preferred_email",
            "current_job_title",
            "target_job_title",
            "current_skills",
            "target_skills",
            "linkedin_account",
            "github_handle",
            "slack_id",
            "phone",
            "texting_ok",
            "time_zone",
        )
        read_only_fields = (
            "uuid",
            "created_at",
            "updated_at",
            "username",
            "email",
        )


class UserProfileSerializer(serializers.ModelSerializer):
    time_zone = TimeZoneSerializerField(use_pytz=False)

    class Meta:
        model = User
        fields = Cru.user_read_fields[profile_value]


class ProjectSerializer(serializers.ModelSerializer):
    """Used to retrieve project info"""

    class Meta:
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
            "google_drive_id",
            "image_logo",
            "image_hero",
            "image_icon",
        )
        read_only_fields = (
            "uuid",
            "created_at",
            "updated_at",
            "completed_at",
        )


class EventSerializer(serializers.ModelSerializer):
    """Used to retrieve event info"""

    class Meta:
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
        read_only_fields = (
            "uuid",
            "created_at",
            "updated_at",
        )


class AffiliateSerializer(serializers.ModelSerializer):
    """Used to retrieve Sponsor Partner info"""

    class Meta:
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
        read_only_fields = (
            "uuid",
            "created_at",
            "updated_at",
        )


class FaqSerializer(serializers.ModelSerializer):
    """Used to retrieve faq info"""

    class Meta:
        model = Faq
        fields = (
            "uuid",
            "question",
            "answer",
            "tool_tip_name",
        )
        read_only_fields = ("uuid", "created_on", "last_updated")


class FaqViewedSerializer(serializers.ModelSerializer):
    """
    Retrieve each date/time the specified FAQ is viewed
    """

    class Meta:
        model = FaqViewed
        fields = (
            "uuid",
            "faq",
        )
        read_only_fields = (
            "uuid",
            "faq",
        )


class LocationSerializer(serializers.ModelSerializer):
    """Used to retrieve Location info"""

    class Meta:
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
        read_only_fields = (
            "uuid",
            "created_at",
            "updated_at",
        )


LocationSerializer._declared_fields["zip"] = serializers.CharField(source="zipcode")


class ProgramAreaSerializer(serializers.ModelSerializer):
    """Used to retrieve program_area info"""

    class Meta:
        model = ProgramArea
        fields = ("uuid", "name", "description", "image")
        read_only_fields = ("uuid", "created_at", "updated_at")


class SkillSerializer(serializers.ModelSerializer):
    """
    Used to retrieve Skill info
    """

    class Meta:
        model = Skill
        fields = (
            "uuid",
            "name",
        )
        read_only_fields = (
            "uuid",
            "created_at",
            "updated_at",
        )


class StackElementSerializer(serializers.ModelSerializer):
    """Used to retrieve stack element info"""

    class Meta:
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
        read_only_fields = (
            "uuid",
            "created_at",
            "updated_at",
        )


class PermissionTypeSerializer(serializers.ModelSerializer):
    """
    Used to retrieve each permission_type info
    """

    class Meta:
        model = PermissionType
        fields = ("uuid", "name", "description")
        read_only_fields = (
            "uuid",
            "created_at",
            "updated_at",
        )


class StackElementTypeSerializer(serializers.ModelSerializer):
    """Used to retrieve stack element types"""

    class Meta:
        model = StackElementType
        fields = (
            "uuid",
            "name",
            "description",
        )
        read_only_fields = (
            "uuid",
            "created_at",
            "updated_at",
        )


class SdgSerializer(serializers.ModelSerializer):
    """
    Used to retrieve Sdg
    """

    class Meta:
        model = Sdg
        fields = (
            "uuid",
            "name",
            "description",
            "image",
        )
        read_only_fields = (
            "uuid",
            "created_at",
            "updated_at",
        )


class AffiliationSerializer(serializers.ModelSerializer):
    """
    Used to retrieve Affiliation
    """

    class Meta:
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
        read_only_fields = ("uuid", "created_at", "updated_at")


class CheckTypeSerializer(serializers.ModelSerializer):
    """
    Used to retrieve check_type info
    """

    class Meta:
        model = CheckType
        fields = ("uuid", "name", "description")
        read_only_fields = ("uuid", "created_at", "updated_at")


class SocMajorSerializer(serializers.ModelSerializer):
    """Used to retrieve soc_major info"""

    class Meta:
        model = SocMajor
        fields = ("uuid", "occ_code", "title")
        read_only_fields = ("uuid", "created_at", "updated_at")
