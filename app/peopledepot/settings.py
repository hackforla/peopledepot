"""
Django settings for peopledepot project.

Generated by 'django-admin startproject' using Django 4.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

# from allauth.account.adapter import DefaultAccountAdapter
import json
import os
from pathlib import Path
from urllib import request

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY")

DJANGO_SUPERUSER_USERNAME = os.environ.get("DJANGO_SUPERUSER_USERNAME")
DJANGO_SUPERUSER_EMAIL = os.environ.get("DJANGO_SUPERUSER_EMAIL")
DJANGO_SUPERUSER_PASSWORD = os.environ.get("DJANGO_SUPERUSER_PASSWORD")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("DEBUG", default=0)

# 'DJANGO_ALLOWED_HOSTS' should be a single string of hosts with a space between each.
# For example: 'DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]'
ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS").split(" ")

# Single sign on
LOGIN_REDIRECT_URL = "/admin/"
# ACCOUNT_LOGOUT_REDIRECT_URL = 'account_login'

# Cognito stuff
COGNITO_AWS_REGION = os.environ.get("COGNITO_AWS_REGION", default=None)
COGNITO_USER_POOL = os.environ.get("COGNITO_USER_POOL", default=None)
COGNITO_USER_POOL_NAME = os.environ.get("COGNITO_USER_POOL_NAME", default=None)
# Provide this value if `id_token` is used for authentication (it contains 'aud' claim).
# `access_token` doesn't have it, in this case keep the COGNITO_AUDIENCE empty
COGNITO_AUDIENCE = os.environ.get("COGNITO_CLIENT_ID", default=None)
COGNITO_POOL_URL = (
    None  # will be set few lines of code later, if configuration provided
)
COGNITO_CLIENT_ID = os.environ.get("COGNITO_CLIENT_ID")
COGNITO_CLIENT_SECRET = os.environ.get("COGNITO_CLIENT_SECRET`")

rsa_keys = {}
# To avoid circular imports, we keep this logic here.
# On django init we download jwks public keys which are used to validate jwt tokens.
# For now there is no rotation of keys (seems like in Cognito decided not to implement it)
if COGNITO_AWS_REGION and COGNITO_USER_POOL:
    COGNITO_POOL_URL = (
        f"https://cognito-idp.{COGNITO_AWS_REGION}.amazonaws.com/{COGNITO_USER_POOL}"
    )
    pool_jwks_url = COGNITO_POOL_URL + "/.well-known/jwks.json"
    jwks = json.loads(request.urlopen(pool_jwks_url).read())  # nosec B310
    rsa_keys = {key["kid"]: json.dumps(key) for key in jwks["keys"]}

# Application definition

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
    "drf_spectacular",
    "phonenumber_field",
    "timezone_field",
    "django_linear_migrations",
    # Local
    "core",
    "data",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    # include the providers you want to enable:
    "allauth.socialaccount.providers.amazon_cognito",
    # autocomplete light
    "dal",
    "dal_select2",
    "queryset_sequence",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.contrib.auth.middleware.RemoteUserMiddleware",
    "allauth.account.middleware.AccountMiddleware",
]

ROOT_URLCONF = "peopledepot.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [Path(BASE_DIR) / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                # `allauth` needs this from django
                "django.template.context_processors.request",
            ],
        },
    },
]

SOCIALACCOUNT_STORE_TOKENS = True
SOCIALACCOUNT_PROVIDERS = {
    "amazon_cognito": {
        "DOMAIN": f"https://{COGNITO_USER_POOL_NAME}.auth.{COGNITO_AWS_REGION}.amazoncognito.com",
        "APP": {
            "client_id": f"{COGNITO_CLIENT_ID}",
            "client_secret": f"{COGNITO_CLIENT_SECRET}",
            "secret": "",
            "key": "",
        },
    },
}
WSGI_APPLICATION = "peopledepot.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": os.environ.get("SQL_ENGINE", "django.db.backends.sqlite3"),
        "NAME": os.environ.get("SQL_DATABASE", BASE_DIR / "db.sqlite3"),
        "USER": os.environ.get("SQL_USER", "user"),
        "PASSWORD": os.environ.get("SQL_PASSWORD", "password"),
        "HOST": os.environ.get("SQL_HOST", "localhost"),
        "PORT": os.environ.get("SQL_PORT", ""),
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "core.User"
ACCOUNT_EMAIL_VERIFICATION = "none"
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.RemoteUserBackend",
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",
    # `allauth` specific authentication methods, such as login by email
    "allauth.account.auth_backends.AuthenticationBackend",
]

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": ("core.api.permissions.DenyAny",),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_jwt.authentication.JSONWebTokenAuthentication",
    ),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}
print("rsa_keys: ", rsa_keys)
JWT_AUTH = {
    "JWT_PAYLOAD_GET_USERNAME_HANDLER": "core.utils.jwt2.get_username_from_payload_handler",
    "JWT_DECODE_HANDLER": "core.utils.jwt2.cognito_jwt_decode_handler",
    "JWT_PUBLIC_KEY": rsa_keys,
    "JWT_ALGORITHM": "RS256",
    "JWT_AUDIENCE": COGNITO_AUDIENCE,
    "JWT_ISSUER": COGNITO_POOL_URL,
    "JWT_AUTH_HEADER_PREFIX": "Bearer",
}

GRAPH_MODELS = {"all_applications": True, "group_models": True}

SPECTACULAR_SETTINGS = {
    "TITLE": "PeopleDepot API",
    "DESCRIPTION": "",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
}
