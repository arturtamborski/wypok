import re
from django.core.validators import RegexValidator

tag_name_validator = RegexValidator(
    r'^[a-zA-Z0-9_]{3,63}$',
    'This field must start with a letter. Length should be between 4 and 20 characters',
    code='invalid'
)
