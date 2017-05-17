from debug_toolbar.settings import PANELS_DEFAULTS
from django.utils.log import DEFAULT_LOGGING
from django.utils import six
from .base import *


LOGGING = DEFAULT_LOGGING

INSTALLED_APPS += [
    'debug_toolbar',
]

MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

DEBUG_TOOLBAR_PANELS = PANELS_DEFAULTS + [
   'debug_toolbar.panels.profiling.ProfilingPanel',
]
