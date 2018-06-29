import datetime


CUSTOM_APPS = [
    'contacts.apps.ContactsConfig',
    'users.apps.UsersConfig',
    'transactions.apps.TransactionsConfig',
    'corsheaders',
    'feedback.apps.FeedbackConfig',
]

CUSTOM_MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware'
]

CORS_ORIGIN_WHITELIST = (
    'hisabkitabin.firebaseapp.com',
    'hisabkitab.in',
)

CSRF_TRUSTED_ORIGINS = CORS_ORIGIN_WHITELIST

CORS_ALLOW_METHODS = (
    'GET',
    'OPTIONS',
    'POST',
)

AUTHENTICATION_BACKENDS = ['users.auth.MultiFieldModelBackend']

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),

    'DEFAULT_AUTHENTICATION_CLASSES': (
        'django_custom_modules.auth.JSONWebTokenAuthenticationQS',
    ),

    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
    ),

    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 100,

    'DEFAULT_FILTER_BACKENDS': (
        'django_custom_modules.serializer.IsOwnerFilterBackend',
        'django_filters.rest_framework.DjangoFilterBackend'
    ),

    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ),
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/day',
        'user': '1000/day'
    }
}

AUTH_USER_MODEL = 'users.User'

JWT_AUTH = {
    'JWT_ENCODE_HANDLER': 'rest_framework_jwt.utils.jwt_encode_handler',

    'JWT_DECODE_HANDLER': 'rest_framework_jwt.utils.jwt_decode_handler',

    'JWT_PAYLOAD_HANDLER': 'django_custom_modules.auth.jwt_payload_handler',

    'JWT_PAYLOAD_GET_USER_ID_HANDLER': 'rest_framework_jwt.utils.jwt_get_user_id_from_payload_handler',

    'JWT_RESPONSE_PAYLOAD_HANDLER': 'rest_framework_jwt.utils.jwt_response_payload_handler',

    # 'JWT_SECRET_KEY': settings.SECRET_KEY,
    'JWT_GET_USER_SECRET_KEY': None,
    'JWT_PUBLIC_KEY': None,
    'JWT_PRIVATE_KEY': None,
    'JWT_ALGORITHM': 'HS512',
    'JWT_VERIFY': True,
    'JWT_VERIFY_EXPIRATION': True,
    'JWT_LEEWAY': 0,
    'JWT_EXPIRATION_DELTA': datetime.timedelta(weeks=4),
    'JWT_AUDIENCE': None,
    'JWT_ISSUER': None,

    # 'JWT_ALLOW_REFRESH': False,
    # 'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=7),

    'JWT_AUTH_HEADER_PREFIX': '',
    # 'JWT_AUTH_COOKIE': None,
}

JWT_AUTH_KEY = 'Authorization'

USE_TZ = False

TIME_ZONE = 'Asia/Kolkata'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = 'static'

JET_THEMES = [
    {
        'theme': 'default',
        'color': '#47bac1',
        'title': 'Default'
    },
    {
        'theme': 'green',
        'color': '#44b78b',
        'title': 'Green'
    },
    {
        'theme': 'light-green',
        'color': '#2faa60',
        'title': 'Light Green'
    },
    {
        'theme': 'light-violet',
        'color': '#a464c4',
        'title': 'Light Violet'
    },
    {
        'theme': 'light-blue',
        'color': '#5EADDE',
        'title': 'Light Blue'
    },
    {
        'theme': 'light-gray',
        'color': '#222',
        'title': 'Light Gray'
    }
]
