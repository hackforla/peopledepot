import uuid

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
    gmail = models.EmailField(blank=True)
    preferred_email = models.EmailField(blank=True)

    # user_status = models.ForeignKey(user_status_type, on_delete=models.PROTECT)
    # current_practice_area = models.ManyToManyField("PracticeArea")
    # target_practice_area = models.ManyToManyField("PracticeArea")

    current_job_title = models.CharField(max_length=255, blank=True)
    target_job_title = models.CharField(max_length=255, blank=True)
    current_skills = models.CharField(max_length=255, blank=True)
    target_skills = models.CharField(max_length=255, blank=True)

    # desired_roles = models.ManyToManyField("Role")
    # availability = models.IntegerField()  # not in ERD, is a separate table. Want to confirm to remove this
    # referred_by = models.ForeignKey(referrer, on_delete=models.PROTECT) # FK
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
    EMAIL_FIELD = "preferred_email"
    REQUIRED_FIELDS = ["email"]  # used only on createsuperuser

    @property
    def is_django_user(self):
        return self.has_usable_password()

    def __str__(self):
        return f"{self.email}"


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
    # current_status_id = models.ForeignKey("status", on_delete=models.PROTECT)
    hide = models.BooleanField(default=True)
    # location_id = models.ForeignKey("location", on_delete=models.PROTECT)
    google_drive_id = models.CharField(max_length=255, blank=True)
    # leads = models.ManyToManyField("lead")
    # leadership_type_id = models.ForeignKey("leadership_type", on_delete=models.PROTECT)
    image_logo = models.URLField(blank=True)
    image_hero = models.URLField(blank=True)
    image_icon = models.URLField(blank=True)

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
    # location_id = models.ForeignKey("Location", on_delete=models.DO_NOTHING)
    # event_type_id = models.ForeignKey("EventType", on_delete=models.DO_NOTHING)
    # brigade_id = models.ForeignKey("Brigade", on_delete=models.DO_NOTHING)
    # day_of_week = models.ForeignKey("DayOfWeek", on_delete=models.DO_NOTHING)
    # must_roles = models.ManyToManyField("Role")
    # should_roles = models.ManyToManyField("Role")
    # could_roles = models.ManyToManyField("Role")
    # frequency_id = models.ForeignKey("Frequency", on_delete=models.DO_NOTHING)

    def __str__(self):
        return f"{self.name}"


class SponsorPartner(AbstractBaseModel):
    """
    Dictionary of sponsors and partners
    """

    partner_name = models.CharField(max_length=255)
    partner_logo = models.URLField(blank=True)
    is_active = models.BooleanField(null=True)
    url = models.URLField(blank=True)
    is_org_sponsor = models.BooleanField(null=True)
    is_org_partner = models.BooleanField(null=True)

    # PK of this model is the ForeignKey for project_partner_xref

    def __str__(self):
        return f"{self.partner_name}"


class Faq(AbstractBaseModel):
    question = models.CharField(max_length=255, unique=True)
    answer = models.CharField(max_length=255, blank=True)
    tool_tip_name = models.CharField(max_length=255, blank=True)

    # PK of this model is the ForeignKey for faq_id

    def __str__(self):
        return f"{self.question}"


class FaqViewed(AbstractBaseModel):
    """
    FaqViewed tracks how many times an FAQ has been viewed by serving as an instance of an FAQ being viewed.
    """

    faq = models.ForeignKey(Faq, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "FAQ view"

    def __str__(self):
        return f"{self.faq} viewed at {self.created_at.strftime('%b %d %Y %H:%M:%S')}"


class Location(AbstractBaseModel):
    """
    Location for event
    """

    name = models.CharField(max_length=255, unique=True, verbose_name="Location name")
    address_line_1 = models.CharField(max_length=255, unique=False)
    address_line_2 = models.CharField(max_length=255, unique=False, blank=True)
    city = models.CharField(max_length=100, unique=False)
    state = models.CharField(max_length=2, unique=False)
    zipcode = models.CharField(max_length=10, unique=False)
    phone = PhoneNumberField(blank=True)

    def __str__(self):
        return f"{self.name}"


class PracticeArea(AbstractBaseModel):
    """
    Practice Area
    """

    name = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.name}"


class ProgramArea(AbstractBaseModel):
    """
    Dictionary of program areas (to be joined with project)
    """

    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    image = models.URLField(blank=True)

    def __str__(self):
        return f"{self.name}"


class Skill(AbstractBaseModel):
    """
    Dictionary of skills
    """

    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name}"


class Technology(AbstractBaseModel):
    """
    Dictionary of technologies used in projects
    """

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    url = models.URLField(blank=True)
    logo = models.URLField(blank=True)
    active = models.BooleanField(null=True)

    # PK of this model is the ForeignKey for project_partner_xref

    class Meta:
        verbose_name_plural = "Technologies"

    def __str__(self):
        return f"{self.name}"


class PermissionType(AbstractBaseModel):
    """
    Permission Type
    """

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        if self.description and isinstance(self.description, str):
            return f"{self.name}: {self.description}"
        else:
            return f"{self.name}"


class StackElementType(AbstractBaseModel):
    """
    Stack element type used to update a shared data store across projects
    """

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    # PK of this model is the ForeignKey for stack_element

    def __str__(self):
        return f"{self.name}"


class Sdg(AbstractBaseModel):
    """
    Dictionary of SDGs
    """

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    image = models.URLField(blank=True)

    # PK of this model is the ForeignKey for sdg_target_indicator

    def __str__(self):
        return f"{self.name}"
