from django.contrib.auth.models import Group
from django.core import serializers
from rest_framework import serializers as rest_serializers
from timezone_field.rest_framework import TimeZoneSerializerField

from core.models import User


class GroupSerializer(rest_serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ("id",)


class SecuredUserSerializer(rest_serializers.ModelSerializer):
    """Used to retrieve user info"""

    time_zone = TimeZoneSerializerField(use_pytz=False)
    # groups = rest_serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    groups = GroupSerializer(many=True, read_only=True)

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
