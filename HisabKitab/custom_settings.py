import datetime
import environ

# sentry config
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False),
    ALLOWED_HOSTS=(list, []),
    CORS_ORIGIN_WHITELIST=(list, []),
    TEMPLATE_DIRS=(list, ["templates"]),
)

# reading .env file
environ.Env.read_env()

# Sentry
sentry_sdk.init(
    dsn=env("SENTRY_DSN"),
    integrations=[DjangoIntegration()],
    environment=env("SENTRY_ENV"),
)

# False if not in os.environ
DEBUG = env("DEBUG")

# SECURITY WARNING: keep the secret key used in production secret!
# Raises django's ImproperlyConfigured exception if SECRET_KEY not in os.environ
SECRET_KEY = env("SECRET_KEY")

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

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

# Email Config
# email config
EMAIL_BACKEND = env("EMAIL_BACKEND")
EMAIL_HOST = env("EMAIL_HOST")
EMAIL_PORT = env("EMAIL_PORT")
EMAIL_HOST_USER = env("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = env("EMAIL_USE_TLS")
EMAIL_FROM = env("DEFAULT_FROM_EMAIL")
DEFAULT_FROM_EMAIL = EMAIL_FROM

CUSTOM_APPS = [
    "usersettings",
    "drf_account",
    "drf_contact",
    "users.apps.UsersConfig",
    "drf_transaction",
    "corsheaders",
    "oauth2_provider",
    "drfaddons",
    "drf_yasg",
    "munsiji",
    "fcm_notification",
]

# FCM_DJANGO_SETTINGS = {
#         "FCM_SERVER_KEY": "[your api key]"
# }
#
# from push_notifications.models import GCMDevice
# devices = GCMDevice.objects.filter(registration_id=)
# devices.send_message("Happy name day!")

CORS_ORIGIN_ALLOW_ALL = True
# CORS_ORIGIN_WHITELIST = env.list("CORS_ORIGIN_WHITELIST")

# CSRF_TRUSTED_ORIGINS = CORS_ORIGIN_WHITELIST

CORS_ALLOW_METHODS = (
    "GET",
    "OPTIONS",
    "POST",
    "PUT",
    "DELETE",
)

LOGIN_REDIRECT_URL = "https://hisabkitab.in/login"

AUTHENTICATION_BACKENDS = [
    "oauth2_provider.backends.OAuth2Backend",
    "users.auth.MultiFieldModelBackend",
]

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "oauth2_provider.contrib.rest_framework.OAuth2Authentication",
        "drfaddons.auth.JSONWebTokenAuthenticationQS",
    ),
    "DEFAULT_PARSER_CLASSES": ("rest_framework.parsers.JSONParser",),
    "DEFAULT_RENDERER_CLASSES": ("rest_framework.renderers.JSONRenderer",),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
    "DEFAULT_FILTER_BACKENDS": (
        "drfaddons.filters.IsOwnerFilterBackend",
        "django_filters.rest_framework.DjangoFilterBackend",
    ),
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

JET_THEMES = [
    {"theme": "default", "color": "#47bac1", "title": "Default"},
    {"theme": "green", "color": "#44b78b", "title": "Green"},
    {"theme": "light-green", "color": "#2faa60", "title": "Light Green"},
    {"theme": "light-violet", "color": "#a464c4", "title": "Light Violet"},
    {"theme": "light-blue", "color": "#5EADDE", "title": "Light Blue"},
    {"theme": "light-gray", "color": "#222", "title": "Light Gray"},
]
