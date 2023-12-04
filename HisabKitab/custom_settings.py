import datetime
import logging
import os

import environ
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.logging import LoggingIntegration
from sentry_sdk.integrations.redis import RedisIntegration

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False),
    ALLOWED_HOSTS=(list, []),
    CORS_ORIGIN_WHITELIST=(list, []),
    TEMPLATE_DIRS=(list, ["templates"]),
)

# reading .env file
environ.Env.read_env()

# False if not in os.environ
DEBUG = env("DEBUG")

# SECURITY WARNING: keep the secret key used in production secret!
# Raises django's ImproperlyConfigured exception if SECRET_KEY not in os.environ
SECRET_KEY = env("SECRET_KEY")

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")

# Email Config
EMAIL_BACKEND = env("EMAIL_BACKEND")
EMAIL_HOST = env("EMAIL_HOST")
EMAIL_PORT = env("EMAIL_PORT")
EMAIL_HOST_USER = env("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = env("EMAIL_USE_TLS")
EMAIL_FROM = env("DEFAULT_FROM_EMAIL")
DEFAULT_FROM_EMAIL = EMAIL_FROM

CUSTOM_APPS = [
    "drf_account",
    "drf_contact",
    "users.apps.UsersConfig",
    "drf_transaction",
    "core.apps.CoreConfig",
    "corsheaders",
    "drfaddons",
    "drf_yasg",
    "huey.contrib.djhuey",
]

CUSTOM_MIDDLEWARE = []
CORS_ORIGIN_ALLOW_ALL = True

CORS_ALLOW_METHODS = (
    "GET",
    "OPTIONS",
    "POST",
    "PUT",
    "DELETE",
)

LOGIN_REDIRECT_URL = "https://hisabkitab.in/login"

AUTHENTICATION_BACKENDS = [
    "users.auth.MultiFieldModelBackend",
]

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_AUTHENTICATION_CLASSES": ("drfaddons.auth.JSONWebTokenAuthenticationQS",),
    "DEFAULT_PARSER_CLASSES": ("rest_framework.parsers.JSONParser",),
    "DEFAULT_RENDERER_CLASSES": ("rest_framework.renderers.JSONRenderer",),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
    "DEFAULT_FILTER_BACKENDS": ("django_filters.rest_framework.DjangoFilterBackend",),
    "DEFAULT_THROTTLE_CLASSES": (
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
    ),
    "DEFAULT_THROTTLE_RATES": {"anon": "100/day", "user": "1000/day"},
}

AUTH_USER_MODEL = "users.User"

JWT_AUTH = {
    "JWT_ENCODE_HANDLER": "rest_framework_jwt.utils.jwt_encode_handler",
    "JWT_DECODE_HANDLER": "rest_framework_jwt.utils.jwt_decode_handler",
    "JWT_PAYLOAD_HANDLER": "rest_framework_jwt.utils.jwt_payload_handler",
    "JWT_PAYLOAD_GET_USER_ID_HANDLER": "rest_framework_jwt.utils.jwt_get_user_id_from_payload_handler",
    "JWT_RESPONSE_PAYLOAD_HANDLER": "rest_framework_jwt.utils.jwt_response_payload_handler",
    # 'JWT_SECRET_KEY': settings.SECRET_KEY,
    "JWT_GET_USER_SECRET_KEY": None,
    "JWT_PUBLIC_KEY": None,
    "JWT_PRIVATE_KEY": None,
    "JWT_ALGORITHM": "HS512",
    "JWT_VERIFY": True,
    "JWT_VERIFY_EXPIRATION": True,
    "JWT_LEEWAY": 0,
    "JWT_EXPIRATION_DELTA": datetime.timedelta(weeks=4),
    "JWT_AUDIENCE": None,
    "JWT_ISSUER": None,
    # 'JWT_ALLOW_REFRESH': False,
    # 'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=7),
    "JWT_AUTH_HEADER_PREFIX": "",
    # 'JWT_AUTH_COOKIE': None,
}

JWT_AUTH_KEY = "Authorization"

USE_TZ = False

TIME_ZONE = "Asia/Kolkata"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = "/static/"

STATIC_ROOT = "static"

# Sentry
# ------------------------------------------------------------------------------
SENTRY_DSN = env("SENTRY_DSN")
SENTRY_LOG_LEVEL = env.int("DJANGO_SENTRY_LOG_LEVEL", logging.INFO)

sentry_logging = LoggingIntegration(
    level=SENTRY_LOG_LEVEL,  # Capture info and above as breadcrumbs
    event_level=logging.ERROR,  # Send errors as events
)
sentry_sdk.init(
    dsn=SENTRY_DSN,
    integrations=[sentry_logging, DjangoIntegration(), RedisIntegration()],
    environment=env("SENTRY_ENV"),
    release=env("SENTRY_RELEASE"),
    traces_sample_rate=float(env("TRACE_SAMPLE_RATE")),
    send_default_pii=True,
    _experiments={
        "profiles_sample_rate": 1.0,
    },
)

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases
if env.bool("USE_SQLITE", default=False):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": env("DB_ENGINE"),
            "NAME": env("DB_NAME"),
            "USER": env("DB_USER"),
            "PASSWORD": env("DB_PASSWORD"),
            "PORT": env("DB_PORT"),
            "HOST": env("DB_HOST"),
        }
    }

REDIS_URL = env.str("REDIS_URL")

# HUEY
HUEY = {
    "name": "HisabKitab",
    "url": REDIS_URL,
    "immediate": DEBUG,
    "utc": False,
    "consumer": {
        "workers": 2,
        "worker_type": "thread",
    },
}

# Welcome Email Configuration
WELCOME_EMAIL_SUBJECT = "New account created | Hisab Kitab"
WELCOME_EMAIL_BODY = """You've successfully created an account on Hisab Kitab. Thank you for
choosing us. We hope you have a great experience with us. If you have any queries,
please create an issue on our GitHub repository at https://github.com/101Loop/HisabKitab-BE/issues
We will try to resolve it as soon as possible. Thank you!

This app is a product of Vitartha, a StartUp focusing on Financially aware India.
Vitartha will also like to thank M/s Civil Machines Technologies Private Limited for the technical
production & development of this app.
Thank You!
"""

ALLOWED_OTP_CHARACTERS = "0123456789"
