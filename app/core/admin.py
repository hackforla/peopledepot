from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from django.contrib.auth.forms import UserChangeForm as DefaultUserChangeForm
from django.contrib.auth.forms import UserCreationForm as DefaultUserCreationForm
from django.contrib.auth.forms import UsernameField
from django.utils.translation import gettext_lazy as _

from .models import Faq
from .models import FaqViewed
from .models import Project
from .models import RecurringEvent
from .models import SponsorPartner
from .models import User
from .models import Location 


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


@admin.register(RecurringEvent)
class RecurringEventAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "start_time",
        "duration_in_min",
    )


@admin.register(SponsorPartner)
class SponsorPartnerAdmin(admin.ModelAdmin):
    list_display = (
        "partner_name",
        "partner_logo",
        "is_active",
        "url",
        "is_sponsor",
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

@admin.register(Location)
class Location(admin.ModelAdmin):
    list_display = (
        "name",
        "address_line_1",
        "address_line_2",
        "city",
        "state",
        "zip",
        "phone"
    )
