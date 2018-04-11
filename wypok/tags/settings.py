from django.conf import settings


MIN_LENGTH              = 3
MAX_LENGTH              = 64
REGEX                   = r'[a-zA-Z0-9_]{' + str(MIN_LENGTH) + r',' + str(MAX_LENGTH) + r'}'

BACKGROUND_PATH        = 'tags/{id}-{name}'
DEFAULT_BACKGROUND     = 'tags/default.jpg'

ALLOWED_CONTENT_TYPES  = settings.ALLOWED_IMAGE_CONTENT_TYPES
