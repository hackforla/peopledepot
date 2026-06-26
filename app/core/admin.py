from django import forms
from django.contrib import admin
from django.contrib.admin.filters import AllValuesFieldListFilter
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from django.contrib.auth.forms import UserChangeForm as DefaultUserChangeForm
from django.contrib.auth.forms import UserCreationForm as DefaultUserCreationForm
from django.contrib.auth.forms import UsernameField
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import Accomplishment
from .models import Affiliate
from .models import Affiliation
from .models import CheckType
from .models import Event
from .models import EventType
from .models import Faq
from .models import FaqViewed
from .models import LeadershipType
from .models import Location
from .models import ModernJobTitle
from .models import Organization
from .models import PermissionType
from .models import PracticeArea
from .models import ProgramArea
from .models import Project
from .models import ProjectStackElementXref
from .models import ProjectStatus
from .models import ProjectUrl
from .models import Referrer
from .models import ReferrerType
from .models import Sdg
from .models import SdgTargetIndicator
from .models import Skill
from .models import SocBroad
from .models import SocDetailed
from .models import SocMajor
from .models import SocMinor
from .models import StackElement
from .models import StackElementType
from .models import UrlStatusType
from .models import UrlType
from .models import User
from .models import UserCheck
from .models import UserEmploymentHistory
from .models import UserPracticeAreaSecondaryXref
from .models import UserStatusType
from .models import Win
from .models import WinType


class UserCreationForm(DefaultUserCreationForm):
    class Meta(DefaultUserCreationForm.Meta):
        model = User


class UserChangeForm(DefaultUserChangeForm):
    class Meta(DefaultUserCreationForm.Meta):
        model = User
        fields = "__all__"
        field_classes = {"username": UsernameField}


class UserAdminForm(UserChangeForm):
    """
    Overrides the ui assignment of a through model from outside of the form to inline.
    Renders secondary practice area menu inline between "practice area primary" and "practice area target intake".
    """

    practice_areas_secondary_virtual = forms.ModelMultipleChoiceField(
        queryset=PracticeArea.objects.all(),
        required=False,
        label="Practice area(s) secondary",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            # Pre-populate the field with the user's existing secondary practice areas.
            self.fields[
                "practice_areas_secondary_virtual"
            ].initial = self.instance.practice_areas_secondary.all()

    def clean(self):
        # Clean to ensure the user's practice area entries aren't duplicates before saving to the xref table.
        cleaned_data = super().clean()
        primary = cleaned_data.get("practice_area_primary")
        secondaries = cleaned_data.get("practice_areas_secondary_virtual")

        if primary and secondaries and primary in secondaries:
            raise ValidationError(
                {
                    "practice_areas_secondary_virtual": (
                        "A practice area cannot be both primary and secondary."
                    )
                }
            )

        return cleaned_data

    def _save_secondary_areas(self, user):
        """Helper to break complex logic out of save() and satisfy linter."""

        # Default to an empty list if user does not have a secondary practice area in xref table.
        selected_areas = self.cleaned_data.get("practice_areas_secondary_virtual", [])

        # Delete existing records between user and practice area in xref table to avoid duplicate entries.
        UserPracticeAreaSecondaryXref.objects.filter(user=user).delete()

        if selected_areas:
            new_xrefs = [
                UserPracticeAreaSecondaryXref(user=user, practice_area=area)
                for area in selected_areas
            ]

            UserPracticeAreaSecondaryXref.objects.bulk_create(new_xrefs)

    def save(self, commit=True):
        """
        Saves the form and handles the custom UserPracticeAreaSecondaryXref bridge table.

        When the Django Admin calls save() with commit=False (e.g., when adding a
        new user that doesn't have a database ID yet), we must delay our bridge
        table updates by hooking them into Django's native save_m2m cleanup process.
        """
        user = super().save(commit=commit)

        if commit:
            self._save_secondary_areas(user)
        else:
            # Stash Django save_m2m function that handles standard fields.
            default_save_m2m = self.save_m2m

            # Add the custom save function to default save_m2m function.
            def new_save_m2m():
                default_save_m2m()
                self._save_secondary_areas(user)

            self.save_m2m = new_save_m2m

        return user


@admin.register(User)
class UserAdmin(DefaultUserAdmin):
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "username",
                    "email",
                    "password",
                )
            },
        ),
        (
            _("Profile"),
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "email_gmail",
                    "email_preferred",
                    "intake_present_job_title",
                    "intake_target_job_titles",
                    "current_target_job_titles",
                    "current_skills",
                    "intake_target_skills",
                    "intake_present_skills",
                    "current_target_skills",
                    "referrer",
                    "linkedin_account",
                    "github_handle",
                    "slack_member_id",
                    "phone",
                    "texting_ok",
                    "time_zone",
                    "practice_area_primary",
                    "practice_area_secondary_virtual",  # Replaces practice_area_secondary due to xref
                    "practice_area_target_intake",
                    "email_cognito",
                    "user_status_type",
                )
            },
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (
            _("Important_dates"),
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )
    readonly_fields = ("username", "email", "created_at", "updated_at")
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "password",
                    "password2",
                ),
            },
        ),
    )
    list_display = ("username", "is_staff", "is_active")
    list_filter = ("username", "email")

    add_form = UserCreationForm
    form = UserAdminForm


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "hide",
        "created_at",
        "updated_at",
        "completed_on",
    )


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "start_time",
        "duration_in_min",
    )


@admin.register(PracticeArea)
class PracticeAreaAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
    )


@admin.register(Affiliate)
class AffiliateAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "logo",
        "is_active",
        "url",
        "is_org_sponsor",
        "is_org_partner",
    )


@admin.register(Faq)
class Faq(admin.ModelAdmin):
    list_display = (
        "question",
        "answer",
        "tool_tip_name",
    )


@admin.register(FaqViewed)
class FaqViewed(admin.ModelAdmin):
    list_display = (
        "faq",
        "read",
    )


@admin.register(LeadershipType)
class LeadershipTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "description")


@admin.register(Location)
class Location(admin.ModelAdmin):
    list_display = (
        "name",
        "address_line_1",
        "address_line_2",
        "city",
        "state",
        "zipcode",
        "phone",
    )


@admin.register(ModernJobTitle)
class ModernJobTitleAdmin(admin.ModelAdmin):
    list_display = ("title", "soc_detailed", "created_at")
    search_fields = ("title",)
    list_filter = ("soc_detailed",)


@admin.register(ProgramArea)
class ProgramAreaAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "image")


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
    )

    list_filter = ("name",)


@admin.register(StackElement)
class StackElementAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
        "url",
        "logo",
        "active",
    )


@admin.register(PermissionType)
class PermissionTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "description")


@admin.register(StackElementType)
class StackElementType(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
    )


@admin.register(Sdg)
class SdgAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "image")


@admin.register(SdgTargetIndicator)
class SdgTargetIndicatorAdmin(admin.ModelAdmin):
    list_display = (
        "sdg",
        "code",
        "description_number",
        "created_at",
    )
    search_fields = ("code", "description_number", "sdg__name")
    list_filter = ("sdg",)


@admin.register(Affiliation)
class AffiliationAdmin(admin.ModelAdmin):
    list_display = (
        "affiliate",
        "project",
        "created_at",
        "ended_at",
        "is_sponsor",
        "is_partner",
    )
    list_filter = ("is_sponsor", "is_partner", "affiliate", "project")


@admin.register(CheckType)
class CheckTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "description")


@admin.register(EventType)
class EventTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "description")


@admin.register(ProjectStatus)
class ProjectStatusAdmin(admin.ModelAdmin):
    list_display = ("name", "description")


@admin.register(SocBroad)
class SocBroadAdmin(admin.ModelAdmin):
    list_display = ("title", "occ_code", "soc_minor")
    list_filter = ("soc_minor",)
    search_fields = ("title", "occ_code")


@admin.register(SocDetailed)
class SocDetailedAdmin(admin.ModelAdmin):
    list_display = ("occ_code", "title", "soc_broad", "created_at")
    search_fields = ("occ_code", "title", "soc_broad__title")
    list_filter = ("soc_broad",)


@admin.register(SocMajor)
class SocMajorAdmin(admin.ModelAdmin):
    list_display = ("occ_code", "title")


@admin.register(SocMinor)
class SocMinorAdmin(admin.ModelAdmin):
    list_display = ("soc_major", "occ_code", "title")


@admin.register(UrlType)
class UrlTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "description")


@admin.register(UserStatusType)
class UserStatusTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "description")


@admin.register(ReferrerType)
class ReferrerTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "description")


@admin.register(Referrer)
class ReferrerAdmin(admin.ModelAdmin):
    list_display = ("name", "url")


@admin.register(ProjectUrl)
class ProjectUrlAdmin(admin.ModelAdmin):
    list_display = (
        "project",
        "url_type",
        "name",
        "external_id",
        "url",
    )


@admin.register(ProjectStackElementXref)
class ProjectStackElementXrefAdmin(admin.ModelAdmin):
    list_display = (
        "project",
        "stack_element",
    )


@admin.register(UrlStatusType)
class UrlStatusTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "description")


@admin.register(Accomplishment)
class AccomplishmentAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "project",
        "accomplished_on",
        "created_at",
    )
    list_filter = ("project", "accomplished_on")


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ("name", "time_zone")
    search_fields = ("name",)
    list_filter = (("time_zone", AllValuesFieldListFilter),)


@admin.register(UserCheck)
class UserCheckAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "check_type",
        "org",
        "project",
        "result",
        "reminder_start",
        "completed_at",
        "created_at",
    )
    search_fields = ("user__username", "check_type__name", "org__name", "project__name")
    list_filter = ("result", "check_type", "org", "project")


@admin.register(UserEmploymentHistory)
class UserEmploymentHistoryAdmin(admin.ModelAdmin):
    list_display = ("user", "title", "soc_detailed", "created_at")
    search_fields = ("title", "user__username", "user__email")
    list_filter = ("soc_detailed",)


@admin.register(Win)
class WinAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "description",
        "win_type",
        "can_use_photo",
        "created_at",
        "updated_at",
    )
    list_filter = ("win_type", "can_use_photo", "user")


@admin.register(WinType)
class WinTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "display_text")
