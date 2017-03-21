import os
from decouple import config, Csv

SITE_ID = 1

ROOT_URLCONF            = 'wypok.urls'
WSGI_APPLICATION        = 'wypok.wsgi.application'
DJANGO_SETTINGS_MODULE  = 'wypok.settings'

BASE_DIR        = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEBUG           = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS   = config('ALLOWED_HOSTS', cast=Csv())
SECRET_KEY      = config('SECRET_KEY')

DB_NAME         = config('DB_NAME')
DB_USER         = config('DB_USER')
DB_PASSWORD     = config('DB_PASSWORD')
DB_HOST         = config('DB_HOST')

if not DEBUG:
    SECURE_PROXY_SSL_HEADER     = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_BROWSER_XSS_FILTER   = True
    SECURE_SSL_REDIRECT         = True
    USE_X_FORWARDED_HOST        = True
    SESSION_COOKIE_SECURE       = True
    SESSION_COOIE_HTTPONLY      = True
    CSRF_COOKIE_SECURE          = True

LANGUAGE_CODE   = 'en-us'
TIME_ZONE       = 'UTC'
USE_I18N        = True
USE_L10N        = True
USE_TZ          = True

STATIC_ROOT     = os.path.join(BASE_DIR, 'static')
STATIC_URL      = '/static/'

INSTALLED_APPS = [
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
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                #'allauth.account.context_processors.account',
                #'allauth.socialaccount.context_processors.socialaccount',
            ],
        },
    },
]

DATABASES = {
    'default': {
        'ENGINE':   'django.db.backends.postgresql_psycopg2',
        'NAME':     DB_NAME,
        'USER':     DB_USER,
        'PASSWORD': DB_PASSWORD,
        'HOST':     DB_HOST,
        'PORT':     '',
    }
}

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'METHOD': 'oauth2',
        'SCOPE': ['profile', 'email'],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    },
}


#AUTH_USER_MODEL     = 'user.Account'
LOGIN_REDIRECT_URL  = '/accounts/me/'
ACCOUNT_AUTHENTICATION_METHOD   = 'username_email'
ACCOUNT_DEFAULT_HTTP_PROTOCOL   = 'https'

#ACCOUNT_USERNAME_VALIDATORS     = accounts.validators.AccountNameValidator
ACCOUNT_USERNAME_MIN_LENGTH     = 4
ACCOUNT_PASSWORD_MIN_LENGTH     = 8

ACCOUNT_EMAIL_REQUIRED          = True
ACCOUNT_EMAIL_VERIFICATION      = 'mandatory'
ACCOUNT_EMAIL_SUBJECT_PREFIX    = 'wypok - '

ACCOUNT_LOGIN_ATTEMPTS_LIMIT    = 3
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT  = 180 # 3 min

ACCOUNT_LOGOUT_ON_PASSWORD_CHANGE = True

ACCOUNT_USERNAME_BLACKLIST = [
    'root',
    'admin',
    'administrator',
    'Administrator',
]
