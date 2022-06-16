import uuid

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.postgres.fields import ArrayField
from django.db import models


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
        return f"<{self.__class__.__name__} {self.uuid}"


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
    # For django-users it will contain username which will be used to login into django-admin site
    username = models.CharField(
        "Username", max_length=255, unique=True, validators=[username_validator]
    )
    is_active = models.BooleanField("Active", default=True)

    # Cognito-user related fields #
    # some additional fields which will be filled-out only for users registered via Cognito
    pass

    # Django-user related fields #
    # password is inherited from AbstractBaseUser
    email = models.EmailField("Email address", blank=True)  # allow non-unique emails
    is_staff = models.BooleanField(
        "staff status",
        default=False,
        help_text="Designates whether the user can log into this admin site.",
    )

    first_name = models.CharField(max_length=255, blank=True, default="")
    last_name = models.CharField(max_length=255, blank=True, default="")
    gmail = models.EmailField(blank=True)
    preferred_email = models.EmailField(blank=True)

    # user_status_id = models.ForeignKey(user_status_type, on_delete=models.SET_DEFAULT, default="inactive") # FK to user_status_type

    # current_practice_area = ArrayField(
    #     models.IntegerField()  # practice area ID, should be FK?
    # )
    # target_practice_area = ArrayField(
    #     models.IntegerField()  # practice area ID, should be FK?
    # )
    current_job_title = models.CharField(max_length=255, blank=True, default="")
    target_job_title = models.CharField(max_length=255, blank=True, default="")
    current_skills = models.CharField(max_length=255, blank=True, default="")
    target_skills = models.CharField(max_length=255, blank=True, default="")

    # desired_roles = ArrayField(models.IntegerField())  # role ID
    # availability = models.IntegerField()  # not in ERD, is a separate table
    # referred_by = models.ForeignKey(referrer, on_delete=models.SET_DEFAULT, default="referrer_deleted") # FK to referrer

    linkedin_account = models.CharField(max_length=255, blank=True, default="")
    github_handle = models.CharField(max_length=255, blank=True, default="")
    slack_id = models.CharField(max_length=11, blank=True, default="")
    phone = models.CharField(max_length=15, blank=True, default="")
    texting_ok = models.BooleanField(default=True)

    time_zone = models.CharField(
        max_length=50, blank=True, default=""
    )  # full timezone name
    # conduct = models.BooleanField()  # not in ERD

    objects = UserManager()

    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["email"]  # used only on createsuperuser

    @property
    def is_django_user(self):
        return self.has_usable_password()
