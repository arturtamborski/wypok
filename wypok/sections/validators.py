import re
from django.core.validators import RegexValidator


section_name_validator = RegexValidator(
    r'^[a-zA-Z][a-zA-Z0-9]{1,19}$',
    'This field can contain only characters a-zA-Z0-9 and be max 20 characters long',
    code='invalid'
)
