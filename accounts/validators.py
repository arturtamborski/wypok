from django.core import validators
import re

class AccountNameValidator(validators.RegexValidator):
    regex   = r'^[a-zA-Z][a-zA-Z0-9-_]{3,19}'
    message = 'Enter a valid username. This value must start with a letter and must be at least 4 characters long, but not longer than 20 characters.'
    flags   = re.ASCII
