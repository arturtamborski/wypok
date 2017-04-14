import os
from decouple import config, Csv

SITE_ID = 1

ROOT_URLCONF            = 'wypok.urls'
WSGI_APPLICATION        = 'wypok.wsgi.application'
DJANGO_SETTINGS_MODULE  = 'wypok.settings'

BASE_DIR                = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

NAME                    = config('NAME', default='Django')
DEBUG                   = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS           = config('ALLOWED_HOSTS', cast=Csv())
SECRET_KEY              = config('SECRET_KEY')

LANGUAGE_CODE           = config('LANGUAGE_ZONE', default='en-us')
TIME_ZONE               = config('TIME_ZONE', default='UTC')
USE_I18N                = True
USE_L10N                = True
USE_TZ                  = True

STATIC_ROOT     = os.path.join(BASE_DIR, 'static')
STATIC_URL      = '/static/'

EMAIL_BACKEND           = 'django.core.mail.backends.console.EmailBackend'
EMAIL_FILE_PATH         = config('EMAIL_FILE_PATH')
EMAIL_SUBJECT_PREFIX    = config('EMAIL_SUBJECT_PREFIX', default=NAME + ' - ')
EMAIL_HOST              = config('EMAIL_HOST', default='localhost')
EMAIL_PORT              = config('EMAIL_PORT', default=25, cast=int)
EMAIL_HOST_USER         = config('EMAIL_USER', default='')
EMAIL_HOST_PASSWORD     = config('EMAIL_PASSWORD', default='')
DEFAULT_FROM_EMAIL      = config('EMAIL_DEFAULT', default=EMAIL_HOST_USER)
SERVER_EMAIL            = config('EMAIL_SERVER', default=EMAIL_HOST_USER)
EMAIL_TIMEOUT           = config('EMAIL_TIMEOUT', default=1, cast=int)
EMAIL_USE_TLS           = config('EMAIL_TLS', default=False, cast=bool)
EMAIL_USE_SSL           = config('EMAIL_SSL', default=False, cast=bool)
EMAIL_SSL_CERTFILE      = config('EMAIL_CERTFILE')
EMAIL_SSL_KEYFILE       = config('EMAIL_KEYFILE')

DB_ENGINE               = config('DB_ENGINE')
DB_NAME                 = config('DB_NAME')
DB_USER                 = config('DB_USER')
DB_PASSWORD             = config('DB_PASSWORD')
DB_HOST                 = config('DB_HOST')
DB_PORT                 = config('DB_PORT', default='')

CACHE_BACKEND           = config('CACHE_BACKEND')
CACHE_LOCATION          = config('CACHE_LOCATION', cast=Csv())
CACHE_TIMEOUT           = config('CACHE_TIMEOUT')
CACHE_PREFIX            = config('CACHE_PREFIX')

#AUTH_USER_MODEL                 = 'accounts.Account'
LOGIN_REDIRECT_URL              = config('LOGIN_REDIRECT_URL', default=None)
ACCOUNT_AUTHENTICATION_METHOD   = config('ACCOUNT_AUTHENTICATION_METHOD', default='username_email')
ACCOUNT_DEFAULT_HTTP_PROTOCOL   = config('ACCOUNT_DEFAULT_HTTP_PROTOCOL', default='http')

ACCOUNT_USERNAME_VALIDATORS     = config('ACCOUNT_USERNAME_VALIDATORS', default=None, cast=Csv())
ACCOUNT_USERNAME_MIN_LENGTH     = config('ACCOUNT_USERNAME_MIN_LENGTH', default=4, cast=int)
ACCOUNT_PASSWORD_MIN_LENGTH     = config('ACCOUNT_PASSWORD_MIN_LENGTH', default=8, cast=int)

ACCOUNT_EMAIL_REQUIRED          = config('ACCOUNT_EMAIL_REQURIED', default=True, cast=bool)
ACCOUNT_EMAIL_VERIFICATION      = config('ACCOUNT_EMAIL_VERIFICATION', default='mandatory')
ACCOUNT_EMAIL_SUBJECT_PREFIX    = config('ACCOUNT_EMAIL_SUBJECT_PREFIX', default=EMAIL_SUBJECT_PREFIX)
ACCOUNT_LOGIN_ATTEMPTS_LIMIT    = config('ACCOUNT_LOGIN_ATTEMPTS_LIMIT', default=3, cast=int)
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT  = config('ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT', default=180, cast=int)
ACCOUNT_LOGOUT_ON_PASSWORD_CHANGE = config('ACCOUNT_LOGOUT_ON_PASSWORD_CHANGE', default=True, cast=bool)
ACCOUNT_USERNAME_BLACKLIST =    config('ACCOUNT_USERNAMES_BLACKLIST', cast=Csv())

if not DEBUG:
    SECURE_PROXY_SSL_HEADER     = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_BROWSER_XSS_FILTER   = True
    SECURE_SSL_REDIRECT         = True
    USE_X_FORWARDED_HOST        = True
    SESSION_COOKIE_SECURE       = True
    SESSION_COOIE_HTTPONLY      = True
    CSRF_COOKIE_SECURE          = True


INSTALLED_APPS = [
    'wypok',
    'accounts',
    'home',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
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
        'OPTIONS': {
            'KEY_PREFIX': CACHE_PREFIX,
        },
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

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'METHOD': 'oauth2',
        'SCOPE': [
            'profile',
            'email'
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        },
    },
}
