"""
Django settings for peopledepot project.

Generated by 'django-admin startproject' using Django 4.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

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

# Cognito stuff
COGNITO_AWS_REGION = os.environ.get("COGNITO_AWS_REGION", default=None)
COGNITO_USER_POOL = os.environ.get("COGNITO_USER_POOL", default=None)
COGNITO_DOMAIN = os.environ.get("COGNITO_DOMAIN", default=None)
# Provide this value if `id_token` is used for authentication (it contains 'aud' claim).
# `access_token` doesn't have it, in this case keep the COGNITO_AUDIENCE empty
COGNITO_AUDIENCE = os.environ.get("COGNITO_CLIENT_ID", default=None)
COGNITO_POOL_URL = (
    None  # will be set few lines of code later, if configuration provided
)
COGNITO_CLIENT_ID = os.environ.get("COGNITO_CLIENT_ID")
COGNITO_CLIENT_SECRET = os.environ.get("COGNITO_CLIENT_SECRET`") or ""
rsa_keys = {}
# To avoid circular imports, we keep this logic here.
# On django init we download jwks public keys which are used to validate jwt tokens.
# For now there is no rotation of keys (seems like in Cognito decided not to implement it)
if COGNITO_AWS_REGION and COGNITO_USER_POOL:
    try:
        COGNITO_POOL_URL = f"https://cognito-idp.{COGNITO_AWS_REGION}.amazonaws.com/{COGNITO_USER_POOL}"
        pool_jwks_url = COGNITO_POOL_URL + "/.well-known/jwks.json"
        jwks = json.loads(request.urlopen(pool_jwks_url).read())  # nosec B310
        rsa_keys = {key["kid"]: json.dumps(key) for key in jwks["keys"]}
    except Exception as e:
        print(f"Error loading JWKS: {e}", COGNITO_POOL_URL)
        raise e
        # return {}
    JWT_AUTH = {
        "JWT_PAYLOAD_GET_USERNAME_HANDLER": "core.utils.jwt.get_username_from_payload_handler",
        "JWT_DECODE_HANDLER": "core.utils.jwt.cognito_jwt_decode_handler",
        "JWT_PUBLIC_KEY": rsa_keys,
        "JWT_ALGORITHM": "RS256",
        "JWT_AUDIENCE": COGNITO_AUDIENCE,
        "JWT_ISSUER": COGNITO_POOL_URL,
        "JWT_AUTH_HEADER_PREFIX": "Bearer",
    }

# Application definition

INSTALLED_APPS = [
    "corsheaders",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # 3rd party
    "django_extensions",
    "rest_framework",
    "rest_framework.authtoken",
    "drf_spectacular",
    "phonenumber_field",
    "timezone_field",
    "django_linear_migrations",
    # Local
    "core",
    "data",
    # allauth requirements
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    # ... include the providers you want to enable:
    "allauth.socialaccount.providers.amazon_cognito",
]

# Allow specific origins (like your React dev and production URLs)
CORS_ALLOWED_ORIGINS = os.getenv("CORS_ALLOWED_ORIGINS").split(" ")

# Optional: Allow credentials (for cookies or tokens)
CORS_ALLOW_CREDENTIALS = True

# Optional: Control which headers are allowed
CORS_ALLOW_HEADERS = [
    "Authorization",
    "Content-Type",
]


SOCIALACCOUNT_PROVIDERS = {
    "amazon_cognito": {
        "DOMAIN": "https://peopledepot.auth.us-east-2.amazoncognito.com",
        "APP": {
            "client_id": f"{COGNITO_CLIENT_ID}",
            "client_secret": f"{COGNITO_CLIENT_SECRET}",
            "secret": "",
            "key": "",
        },
        "AUTH_PARAMS": {
            "scope": "openid profile email",
        },
        "OAUTH2_CLIENT_CLASS": "allauth.socialaccount.providers.oauth2.client.OAuth2Client",
    }
}
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.auth.middleware.RemoteUserMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
]

ROOT_URLCONF = "peopledepot.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # next comment is to ignore flake8 error for the following line when pre-commit runs
        # flake8: noqa
        "DIRS": [os.path.join(BASE_DIR, "templates")],
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
        "PORT": os.environ.get("SQL_PORT", "5432"),
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

JWT_AUTH = {
    "JWT_PAYLOAD_GET_USERNAME_HANDLER": "core.utils.jwt_handler.get_username_from_payload_handler",
    "JWT_DECODE_HANDLER": "core.utils.jwt_handler.cognito_jwt_decode_handler",
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
