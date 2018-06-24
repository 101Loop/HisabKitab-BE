# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'YOUR SECRET KEY'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'HisabKitabDB',
        'USER': '---',
        'PASSWORD': '---',
    }
}

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.____'
EMAIL_PORT = 465
EMAIL_HOST_USER = '____'
EMAIL_HOST_PASSWORD = '_____'
EMAIL_USE_SSL = True
EMAIL_FROM = "'Flexy Managers | Civil Machines Technologies Private Limited'<admin@civilmachines.com>"
