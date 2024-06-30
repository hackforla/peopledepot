from django.contrib.auth.models import Group
from rest_framework import serializers
from timezone_field.rest_framework import TimeZoneSerializerField

from core.models import Affiliate
from core.models import Affiliation
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
from core.models import StackElementType
from core.models import Technology
from core.models import User


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


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ("id", "name")


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model.

    Parameters:
    - include_groups (bool): Flag to include user groups in the serialized output.
    """

    time_zone = TimeZoneSerializerField(use_pytz=False)
    # see get_groups method
    groups = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "uuid",
            "username",
            "created_at",
            "updated_at",
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
            "groups",
        )
        read_only_fields = (
            "uuid",
            "created_at",
            "updated_at",
            "username",
            "email",
        )

    def get_groups(self, obj):
        include_groups = self.context.get("include_groups", False)
        if include_groups:
            return GroupSerializer(obj.groups.all(), many=True).data
        return None


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


class TechnologySerializer(serializers.ModelSerializer):
    """Used to retrieve technology info"""

    class Meta:
        model = Technology
        fields = (
            "uuid",
            "name",
            "description",
            "url",
            "logo",
            "active",
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
