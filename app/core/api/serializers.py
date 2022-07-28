from rest_framework import serializers

from core.models import User


class UserSerializer(serializers.ModelSerializer):
    """Used to retrieve user info"""

    class Meta:
        model = User
        fields = (
            "username",
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
        )
        read_only_fields = (
            "username",
            "email",
        )
