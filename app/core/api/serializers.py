from rest_framework import serializers
from timezone_field.rest_framework import TimeZoneSerializerField

from core.models import Faq
from core.models import FaqViewed
from core.models import Location
from core.models import PracticeArea
from core.models import ProgramArea
from core.models import Project
from core.models import RecurringEvent
from core.models import Skill
from core.models import SponsorPartner
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


class UserSerializer(serializers.ModelSerializer):
    """Used to retrieve user info"""

    time_zone = TimeZoneSerializerField(use_pytz=False)

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
        )
        read_only_fields = (
            "uuid",
            "created_at",
            "updated_at",
            "username",
            "email",
        )


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
            "github_primary_url",
            "hide",
            "slack_url",
            "google_drive_url",
            "google_drive_id",
            "hfla_website_url",
            "image_logo",
            "image_hero",
            "image_icon",
            "readme_url",
            "wiki_url",
        )
        read_only_fields = (
            "uuid",
            "created_at",
            "updated_at",
            "completed_at",
        )


class RecurringEventSerializer(serializers.ModelSerializer):
    """Used to retrieve recurring_event info"""

    class Meta:
        model = RecurringEvent
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


class SponsorPartnerSerializer(serializers.ModelSerializer):
    """Used to retrieve Sponsor Partner info"""

    class Meta:
        model = SponsorPartner
        fields = (
            "uuid",
            "partner_name",
            "partner_logo",
            "is_active",
            "url",
            "is_sponsor",
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
