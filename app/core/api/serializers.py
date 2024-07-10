from rest_framework import serializers
from timezone_field.rest_framework import TimeZoneSerializerField

from core.field_permissions import FieldPermissions
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
from core.models import UserPermissions
from core.permission_util import PermissionUtil


class PracticeAreaSerializer(serializers.ModelSerializer):
    """Used to determine practice area fields included in a response"""

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


class UserPermissionsSerializer(serializers.ModelSerializer):
    """Used to determine user permission fields included in a response"""

    class Meta:
        model = UserPermissions
        fields = (
            "uuid",
            "created_at",
            "updated_at",
            "user",
            "permission_type",
            "project",
            "practice_area",
        )


class ProfileSerializer(serializers.ModelSerializer):
    """Used to determine user fields included in a response for the me endpoint"""

    time_zone = TimeZoneSerializerField(use_pytz=False)

    class Meta:
        model = User

        # to_representation overrides the need for fields
        # if fields is removed, syntax checker will complain
        fields = "__all__"

    def to_representation(self, instance):
        """Determine which fields are included in a response based on
        the requesting user's permissions

        Args:
            response_user (user): user being returned in the response

        Raises:
            PermissionError: Raised if the requesting user does not have permission to view the target user

        Returns:
            Representation of the user with only the fields that the requesting user has permission to view
        """
        representation = super().to_representation(instance)
        request = self.context.get("request")
        requesting_user: User = request.user
        target_user: User = instance
        if requesting_user != target_user:
            raise PermissionError("You can only use profile endpoint for your own user")
        if request.method != "GET":
            return representation

        new_representation = {}
        for field_name in FieldPermissions.fields_list["me"]["R"]:
            new_representation[field_name] = representation[field_name]
        return new_representation


class UserSerializer(serializers.ModelSerializer):
    """Used to determine user fields included in a response for the user endpoint"""

    time_zone = TimeZoneSerializerField(use_pytz=False)

    class Meta:
        model = User

        # to_representation overrides the need for fields
        # if fields is removed, syntax checker will complain
        fields = "__all__"

    @staticmethod
    def _get_read_fields(__cls__, requesting_user: User, target_user: User):
        highest_ranked_name = UserSerializer._get_highest_ranked_permission_type(
            requesting_user, target_user
        )
        return FieldPermissions.fields_list["user"][highest_ranked_name]["R"]

    def to_representation(self, response_user):
        """Determine which fields are included in a response based on
        the requesting user's permissions

        Args:
            response_user (user): user being returned in the response

        Raises:
            PermissionError: Raised if the requesting user does not have permission to view the target user

        Returns:
            Representation of the user with only the fields that the requesting user has permission to view
        """
        request = self.context.get("request")
        representation = super().to_representation(response_user)
        requesting_user: User = request.user
        target_user: User = response_user

        highest_ranked_name = PermissionUtil.get_lowest_ranked_permission_type(
            requesting_user, target_user
        )
        if highest_ranked_name == "":
            raise PermissionError("You do not have permission to view this user")

        new_representation = {}
        print("Debug 1", FieldPermissions.fields_list["user"])
        print("Debug 2", FieldPermissions.fields_list["user"][highest_ranked_name])
        print("Debug 3", FieldPermissions.fields_list["user"][highest_ranked_name]["R"])
        for field_name in FieldPermissions.fields_list["user"][highest_ranked_name][
            "R"
        ]:
            print("Debug 4", field_name)
            new_representation[field_name] = representation[field_name]
        print("Debug 5")
        return new_representation


class ProjectSerializer(serializers.ModelSerializer):
    """Used to determine user project fields included in a response"""

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
    """Used to determine event fields included in a response"""

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
    """Used to determine affiliate / sponsor partner fields included in a response"""

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
    """Used to determine faq fields included in a response"""

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
    """Used to determine faq viewed fields included in a response

    faq viewed is a table that holds the faq history
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
    """Used to determine location fields included in a response"""

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
    """Used to determine program area fields included in a response"""

    class Meta:
        model = ProgramArea
        fields = ("uuid", "name", "description", "image")
        read_only_fields = ("uuid", "created_at", "updated_at")


class SkillSerializer(serializers.ModelSerializer):
    """Used to determine skill fields included in a response"""

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
    """Used to determine location fields included in a response"""

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
    Used to determine each permission_type info
    """

    class Meta:
        model = PermissionType
        fields = ("uuid", "name", "description", "rank")
        read_only_fields = (
            "uuid",
            "created_at",
            "updated_at",
        )


class StackElementTypeSerializer(serializers.ModelSerializer):
    """Used to determine stack element types"""

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
    Used to determine Sdg
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
    Used to determine Affiliation
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
