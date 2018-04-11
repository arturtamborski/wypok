from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator

from wypok.validators import FileValidator

from . import settings


name_validator = RegexValidator(
    regex = r'^' + settings.REGEX + r'$',
    message = _('tag_name_validator failed'),
)


background_validator = FileValidator(
    content_types = settings.ALLOWED_CONTENT_TYPES
)
