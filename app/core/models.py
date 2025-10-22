import uuid

from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from timezone_field import TimeZoneField


class AbstractBaseModel(models.Model):
    """
    Base abstract model, that has `uuid` instead of `id` and included `created_at`, `updated_at` fields.
    """

    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    created_at = models.DateTimeField("Created at", auto_now_add=True)
    updated_at = models.DateTimeField("Updated at", auto_now=True)

    class Meta:
        abstract = True

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.uuid}>"


class LeadershipType(AbstractBaseModel):
    """
    Dictionary of leadership types to be associated with a project
    """

    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name}"


class User(PermissionsMixin, AbstractBaseUser, AbstractBaseModel):
    """
    Table contains cognito-users & django-users.

    PermissionsMixin leverages the built-in django model permissions system
    (which allows to limit information for staff users via Groups).
    Note: Django-admin user and app user are not split in different tables because of simplicity of development.
    Some libraries assume there is only one user model, and they can't work with both.
    For example, to have a history log of changes for entities - to save which
    user made a change of object attribute, perhaps, auth-related libs, and some
    other.
    With current implementation, we don't need to fork, adapt and maintain third party packages.
    They should work out of the box.
    The disadvantage is - cognito-users will have unused fields which always empty. Not critical.
    """

    username_validator = UnicodeUsernameValidator()

    # Common fields #
    # For cognito-users username will contain `sub` claim from jwt token
    # (unique identifier (UUID) for the authenticated user).
    # For django-users it will contain username which will be used to login
    # into django-admin site
    username = models.CharField(
        "Username", max_length=255, unique=True, validators=[username_validator]
    )
    is_active = models.BooleanField("Active", default=True)

    # Cognito-user related fields #
    # some additional fields which will be filled-out only for users
    # registered via Cognito
    pass

    # Django-user related fields #
    # password is inherited from AbstractBaseUser
    email = models.EmailField("Email address", blank=True)  # allow non-unique emails
    is_staff = models.BooleanField(
        "staff status",
        default=False,
        help_text="Designates whether the user can log into this admin site.",
    )

    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    email_gmail = models.EmailField(blank=True)
    email_preferred = models.EmailField(blank=True)
    email_cognito = models.EmailField(blank=True)

    user_status = models.ForeignKey(
        "UserStatusType", null=True, on_delete=models.PROTECT
    )
    practice_area_primary = models.ForeignKey(
        "PracticeArea",
        related_name="primary_users",
        blank=True,
        null=True,
        on_delete=models.PROTECT,
    )
    practice_area_secondary = models.ManyToManyField(
        "PracticeArea", related_name="secondary_users", blank=True
    )
    practice_area_target_intake = models.ManyToManyField(
        "PracticeArea", related_name="target_intake_users", blank=True
    )

    job_title_current_intake = models.CharField(max_length=255, blank=True)
    job_title_target_intake = models.CharField(max_length=255, blank=True)
    current_skills = models.CharField(max_length=255, blank=True)
    target_skills = models.CharField(max_length=255, blank=True)

    # desired_roles = models.ManyToManyField("Role")
    # availability = models.IntegerField()  # not in ERD, is a separate table. Want to confirm to remove this
    referrer = models.ForeignKey("Referrer", null=True, on_delete=models.PROTECT)  # FK
    # to referrer

    linkedin_account = models.CharField(max_length=255, blank=True)
    github_handle = models.CharField(max_length=255, blank=True)
    slack_id = models.CharField(max_length=11, blank=True)

    phone = PhoneNumberField(blank=True)

    texting_ok = models.BooleanField(default=True)

    time_zone = TimeZoneField(blank=True, use_pytz=False, default="America/Los_Angeles")
    # conduct = models.BooleanField()  # not in ERD. Maybe we should remove
    # this

    objects = UserManager()

    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email_preferred"
    REQUIRED_FIELDS = ["email"]  # used only on createsuperuser

    @property
    def is_django_user(self):
        return self.has_usable_password()

    def __str__(self):
        return f"{self.email}"


class ProjectStatus(AbstractBaseModel):
    """
    Dictionary of status options for project
    """

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "project statuses"

    def __str__(self):
        return f"{self.name}"


class Project(AbstractBaseModel):
    """
    List of projects
    """

    name = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=255, blank=True)
    completed_at = models.DateTimeField("Completed at", null=True, blank=True)
    github_org_id = models.CharField(
        max_length=8,
        blank=True,
        help_text='Can be retrieved from gh api with the following: curl -H \
"Authorization: token [gh_PAT]" https://api.github.com/orgs/[org]',
    )
    github_primary_repo_id = models.CharField(
        max_length=9,
        blank=True,
        help_text='Can be retrieved from gh api with the following: curl -H \
"Authorization: token [gh_PAT]" \
https://api.github.com/repos/[org]/[repo]',
    )
    current_status = models.ForeignKey(
        ProjectStatus, null=True, on_delete=models.PROTECT
    )
    hide = models.BooleanField(default=True)
    # location_id = models.ForeignKey("location", on_delete=models.PROTECT)
    google_drive_id = models.CharField(max_length=255, blank=True)
    # leads = models.ManyToManyField("lead")
    leadership_type = models.ForeignKey(
        LeadershipType, blank=True, null=True, on_delete=models.PROTECT
    )
    image_logo = models.URLField(blank=True)
    image_hero = models.URLField(blank=True)
    image_icon = models.URLField(blank=True)
    sdgs = models.ManyToManyField(
        "Sdg", related_name="projects", blank=True, through="ProjectSdgXref"
    )
    program_areas = models.ManyToManyField(
        "ProgramArea",
        related_name="projects",
        blank=True,
        through="ProjectProgramAreaXref",
    )
    stack_elements = models.ManyToManyField(
        "StackElement",
        through="ProjectStackElementXref",
        related_name="projects",
        blank=True,
    )

    def __str__(self):
        return f"{self.name}"


class Event(AbstractBaseModel):
    """
    Events
    """

    name = models.CharField(max_length=255)
    start_time = models.TimeField("Start", null=True, blank=True)
    duration_in_min = models.IntegerField(null=True, blank=True)
    video_conference_url = models.URLField(blank=True)
    additional_info = models.TextField(blank=True)

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    must_attend = models.JSONField(default=list)
    should_attend = models.JSONField(default=list)
    could_attend = models.JSONField(default=list)
    # location_id = model


class Permission(AbstractBaseModel):
    """
    Defines user permissions for various parts of the application,
    such as projects or practice areas.
    """

    # Renamed from user_id
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # Renamed from project_id
    project = models.ForeignKey(
        Project, null=True, blank=True, on_delete=models.CASCADE
    )

    # Renamed from permission_type_id.
    # TODO: Uncomment when issue #24 is resolved.
    # permission_type = models.ForeignKey('permission_type.PermissionType', on_delete=models.CASCADE)

    # Renamed from practice_area_id.
    # TODO: Uncomment when issue #63 is resolved.
    # practice_area = models.ForeignKey('practice_area.PracticeArea', null=True, blank=True, on_delete=models.CASCADE)

    # New fields
    granted = models.DateTimeField(auto_now_add=True)
    ended = models.DateTimeField(null=True, blank=True)

    # TODO: Uncomment when issues #15, #429, #172 are resolved.
    # created_by = models.ForeignKey(
    #     settings.AUTH_USER_MODEL,
    #     on_delete=models.CASCADE,
    #     related_name='permissions_created'
    # )

    # TODO: Uncomment when issues #15, #429, #172 are resolved.
    # updated_by = models.ForeignKey(
    #     settings.AUTH_USER_MODEL,
    #     on_delete=models.CASCADE,
    #     related_name='permissions_updated',
    #     null=True,
    #     blank=True
    # )

    class Meta:
        db_table = "permission"

    def __str__(self):
        return f"Permission for {self.user} on {self.project or 'Practice Area'}"
