import os
from decouple import config, Csv

ROOT_URLCONF        = 'wypok.urls'
WSGI_APPLICATION    = 'wypok.wsgi.application'

BASE_DIR        = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEBUG           = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS   = config('ALLOWED_HOSTS', cast=Csv())
SECRET_KEY      = config('SECRET_KEY')

DB_NAME         = config('DB_NAME')
DB_USER         = config('DB_USER')
DB_PASSWORD     = config('DB_PASSWORD')
DB_HOST         = config('DB_HOST')

if not DEBUG:
    SECURE_BROWSER_XSS_FILTER   = True
    SECURE_PROXY_SSL_HEADER     = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT         = True
    USE_X_FORWARDED_HOST        = True
    SESSION_COOKIE_SECURE       = True
    SESSION_COOIE_HTTPONLY      = True
    CSRF_COOKIE_SECURE          = True

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'user',
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
            ],
        },
    },
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD': DB_PASSWORD,
        'HOST': DB_HOST,
        'PORT': '',
    }
}

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

LANGUAGE_CODE   = 'en-us'
TIME_ZONE       = 'UTC'
USE_I18N        = True
USE_L10N        = True
USE_TZ          = True

STATIC_ROOT     = os.path.join(BASE_DIR, 'static')
STATIC_URL      = '/static/'
