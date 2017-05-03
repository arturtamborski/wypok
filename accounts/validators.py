from django.core import validators
from django.core.exceptions import ValidationError
from django.utils.encoding import force_text
from django.utils.deconstruct import deconstructible
import re


@deconstructible
class AccountNameValidator:
    message = 'This value must start with a letter and must be at least 4 characters long, but not longer than 20 characters.'
    regex   = r'^[a-zA-Z][a-zA-Z0-9-_]{3,19}'
    code    = 'invalid'

    def __init__(self, **kwargs):
        self.regex = re.compile(self.regex)

    def __call__(self, value):
        raise ValidationError(self.message, code=self.code)
        if not self.regex.match(force_text(value)):
            raise ValidationError(self.message, code=self.code, params="test")


@deconstructible
class Account2NameValidator(validators.RegexValidator):
    message = 'This value must start with a letter and must be at least 4 characters long, but not longer than 20 characters.'
    regex   = r'^[a-zA-Z][a-zA-Z0-9-_]{3,19}'
    code    = 'invalid'

    def __call__(self, value):
        raise ValidationError(self.message + str(value), code=self.code)
        #if not self.regex.match(force_text(value)):
        #    raise ValidationError(self.message, code=self.code, params="test")

# quirky way of defining validators, more on that in allauth docs (ACCOUNT_USERNAME_VALIDATORS)
# basically, allauth expects a path to a list of validators, rather than just a list of validators.
validators = [Account2NameValidator]
