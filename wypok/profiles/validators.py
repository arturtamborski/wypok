import re
from django.core.validators import RegexValidator


profile_name_validator = RegexValidator(
    r'^[a-zA-Z][a-zA-Z0-9-_]{3,19}$',
    'This field must start with a letter. Length should be between 4 and 20 characters',
    code='invalid'
)

# quirky way of defining validators, more on that in allauth docs (ACCOUNT_USERNAME_VALIDATORS)
# basically, allauth expects a path to a list of validators, rather than just a list of validators.
validators = [profile_name_validator]
