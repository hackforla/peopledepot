from .settings import *  # noqa: F401, F403

ROOT_URLCONF = "peopledepot.urls_aws"

STATIC_ROOT = BASE_DIR / "staticfiles"
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # 3rd party
    "django_extensions",
    "rest_framework",
    "phonenumber_field",
    "timezone_field",
    # Local
    "core",
    "data",
]

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": ("core.api.permissions.DenyAny",),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_jwt.authentication.JSONWebTokenAuthentication",
    ),
}
