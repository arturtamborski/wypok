from os import path, environ
from datetime import datetime
from decouple import config, Csv

# Main settings
SITE_ID                     = 1
NAME                        = config('NAME')
BASE_DIR                    = config('BASE_DIR')
ROOT_URLCONF                = config('APP_NAME') + '.urls'
WSGI_APPLICATION            = config('APP_NAME') + '.wsgi' + '.application'
SECRET_KEY                  = config('SECRET_KEY')
DEBUG                       = config('DEBUG', cast=bool)
LOG_LEVEL                   = 'DEBUG' if DEBUG else 'INFO'
INTERNAL_IPS                = config('INTERNAL_IPS', cast=Csv())
ALLOWED_HOSTS               = ['127.0.0.1', 'localhost'] if DEBUG else config('ALLOWED_HOSTS', cast=Csv())
SCHEME                      = 'http' if DEBUG else 'https'
FQDN                        = ALLOWED_HOSTS[0]

# Globalization
LANGUAGE_CODE               = 'en-us'
TIME_ZONE                   = 'UTC'
USE_I18N                    = True
USE_L10N                    = True
USE_TZ                      = True
LANGUAGES                   = [('en', 'English'), ('pl', 'Polish')]

# Static and media
STATIC_ROOT                 = path.join(BASE_DIR, 'static')
STATIC_URL                  = '/static/'
MEDIA_ROOT                  = path.join(BASE_DIR, 'media')
MEDIA_URL                   = '/media/'
FILE_UPLOAD_PERMISSIONS     = 0o644
FILE_UPLOAD_MAX_MEMORY_SIZE = (1024 * 1024) * 5 # 5.MB
DATA_UPLOAD_MAX_MEMORY_SIZE = FILE_UPLOAD_MAX_MEMORY_SIZE

# Email
DEFAULT_FROM_EMAIL          = 'wypok@' + FQDN
SERVER_EMAIL                = 'server@' + FQDN
EMAIL_BACKEND               = config('EMAIL_BACKEND')
EMAIL_HOST_USER             = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD         = config('EMAIL_HOST_PASSWORD')
EMAIL_HOST                  = config('EMAIL_HOST')
EMAIL_PORT                  = config('EMAIL_PORT')
EMAIL_USE_TLS               = config('EMAIL_USE_TLS', cast=bool)
EMAIL_USE_SSL               = config('EMAIL_USE_SSL', cast=bool)
EMAIL_SSL_CERTFILE          = config('EMAIL_SSL_CERTFILE')
EMAIL_SSL_KEYFILE           = config('EMAIL_SSL_KEYFILE')
EMAIL_TIMEOUT               = config('EMAIL_TIMEOUT', cast=int)
EMAIL_FILE_PATH             = config('EMAIL_FILE_PATH')
EMAIL_SUBJECT_PREFIX        = NAME + ' - '

if EMAIL_FILE_PATH[0] != '/':
    EMAIL_FILE_PATH = path.join(BASE_DIR, EMAIL_FILE_PATH)

# Database
DB_ENGINE                   = config('DB_ENGINE')
DB_NAME                     = config('DB_NAME')
DB_USER                     = config('DB_USER')
DB_PASSWORD                 = config('DB_PASSWORD')
DB_HOST                     = config('DB_HOST')
DB_PORT                     = config('DB_PORT')

# Cache
CACHE_BACKEND               = config('CACHE_BACKEND')
CACHE_LOCATION              = config('CACHE_LOCATION', cast=Csv())
CACHE_KEY_PREFIX            = config('CACHE_KEY_PREFIX')
CACHE_TIMEOUT               = config('CACHE_TIMEOUT', cast=int)
CACHE_TTL                   = config('CACHE_TTL', cast=int)

# Accounts
LOGIN_URL                   = 'account_login'
LOGIN_REDIRECT_URL          = 'sections:home'
LOGOUT_REDIRECT_URL         = 'sections:home'

ACCOUNT_LOGIN_ON_PASSWORD_RESET = True
ACCOUNT_LOGOUT_ON_GET           = True
ACCOUNT_LOGOUT_ON_PASSWORD_CHANGE = True

ACCOUNT_ADAPTER                 = 'allauth.account.adapter.DefaultAccountAdapter'
SOCIALACCOUNT_ADAPTER           = 'allauth.socialaccount.adapter.DefaultSocialAccountAdapter'

ACCOUNT_DEFAULT_HTTP_PROTOCOL   = SCHEME
ACCOUNT_AUTHENTICATION_METHOD   = 'username_email'
ACCOUNT_USERNAME_MIN_LENGTH     = 4
ACCOUNT_USERNAME_VALIDATORS     = 'accounts.validators.validators'
ACCOUNT_USERNAME_BLACKLIST      = []

ACCOUNT_EMAIL_REQUIRED          = True
ACCOUNT_UNIQUE_EMAIL            = True
ACCOUNT_EMAIL_VERIFICATION      = 'mandatory'
ACCOUNT_EMAIL_SUBJECT_PREFIX    = EMAIL_SUBJECT_PREFIX

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': ['profile', 'email'],
        'AUTH_PARAMS': {
            'access_type': 'online',
        },
    },
    'facebook': {
        'SCOPE': ['public_profile', 'email'],
        'FIELDS': ['email', 'name', 'verified', 'gender'],
    },
}

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

AUTH_PASSWORD_VALIDATORS = [
    { 'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',

    'sections',
    'accounts',
    'wypok',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.facebook',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    #'django.middleware.cache.UpdateCacheMiddleware',
    #'django.middleware.common.CommonMiddleware',
    #'django.middleware.cache.FetchFromCacheMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.template.context_processors.request',
                'django.contrib.messages.context_processors.messages',
                #'allauth.account.context_processors.account',
                #'allauth.socialaccount.context_processors.socialaccount',
                'sections.context_processors.sections',
            ],
        },
    },
]

DATABASES = {
    'default': {
        'ENGINE':   DB_ENGINE,
        'NAME':     DB_NAME,
        'USER':     DB_USER,
        'PASSWORD': DB_PASSWORD,
        'HOST':     DB_HOST,
        'PORT':     DB_PORT,
    },
}

CACHES = {
    'default': {
        'BACKEND':  CACHE_BACKEND,
        'LOCATION': CACHE_LOCATION,
        'TIMEOUT':  CACHE_TIMEOUT,
        'KEY_PREFIX': CACHE_KEY_PREFIX,
    },
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': LOG_LEVEL,
            'class': 'logging.FileHandler',
            'filename': path.join(BASE_DIR, 'logs', 'django.log'),
        },
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': LOG_LEVEL,
            'propagate': True,
        },
    },
}
