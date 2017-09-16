from wypok.settings.base import *


CSRF_COOKIE_SECURE          = True
USE_X_FORWARDED_HOST        = True
SECURE_SSL_REDIRECT         = True
SECURE_BROWSER_XSS_FILTER   = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_PROXY_SSL_HEADER     = ('HTTP_X_FORWARDED_PROTO', 'https')
CSRF_COOKIE_DOMAIN          = FQDN
CSRF_COOKIE_SECURE          = True

SESSION_COOKIE_DOMAIN       = FQDN
SESSION_COOKIE_HTTPONLY     = True
SESSION_COOKIE_SECURE       = True
SESSION_ENGINE              = 'django.contrib.sessions.backends.cache'
#SESSION_ENGINE              = 'django.contrib.sessions.backends.db'
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
