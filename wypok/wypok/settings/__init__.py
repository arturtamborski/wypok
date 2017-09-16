from os import environ
from decouple import config


if config('DEBUG', cast=bool):
    from .devel import *
    mode = 'devel'
else:
    from .prod import *
    mode = 'prod'

DJANGO_SETTINGS_MODULE = config('APP_NAME') + '.settings.' + mode
environ.setdefault('DJANGO_SETTINGS_MODULE', DJANGO_SETTINGS_MODULE)
