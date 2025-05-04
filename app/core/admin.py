from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from django.contrib.auth.forms import UserChangeForm as DefaultUserChangeForm
from django.contrib.auth.forms import UserCreationForm as DefaultUserCreationForm
from django.contrib.auth.forms import UsernameField
from django.utils.translation import gettext_lazy as _

from .models import Affiliate
from .models import Affiliation
from .models import CheckType
from .models import Event
from .models import EventType
from .models import Faq
from .models import FaqViewed
from .models import LeadershipType
from .models import Location
from .models import PermissionType
from .models import PracticeArea
from .models import ProgramArea
from .models import Project
from .models import ProjectStatus
from .models import Referrer
from .models import ReferrerType
from .models import Sdg
from .models import Skill
from .models import SocMajor
from .models import StackElement
from .models import StackElementType
from .models import UrlType
from .models import User
from .models import UserStatusType


class UserCreationForm(DefaultUserCreationForm):
    class Meta(DefaultUserCreationForm.Meta):
        model = User


class UserChangeForm(DefaultUserChangeForm):
    class Meta(DefaultUserCreationForm.Meta):
        model = User
        fields = "__all__"
        field_classes = {"username": UsernameField}


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
                    "gmail",
                    "preferred_email",
                    "current_job_title",
                    "target_job_title",
                    "current_skills",
                    "target_skills",
                    "referrer",
                    "linkedin_account",
                    "github_handle",
                    "slack_id",
                    "phone",
                    "texting_ok",
                    "time_zone",
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
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ("username", "is_staff", "is_active")
    list_filter = ("username", "email")


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "hide",
        "created_at",
        "updated_at",
        "completed_at",
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
        "partner_name",
        "partner_logo",
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
    list_display = ("faq",)


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


@admin.register(SocMajor)
class SocMajorAdmin(admin.ModelAdmin):
    list_display = ("occ_code", "title")


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
