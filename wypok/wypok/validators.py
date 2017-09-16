from django.template.defaultfilters import filesizeformat
from django.utils.deconstruct import deconstructible
from django.core.exceptions import ValidationError
from django.conf import settings
import magic


MAX_SIZE = getattr(settings, 'FILE_UPLOAD_MAX_MEMORY_SIZE', 2621440)
MIN_SIZE = getattr(settings, 'FILE_UPLOAD_MIN_MEMORY_SIZE', 1024)
CONTENT_TYPES = getattr(settings, 'ALLOWED_CONTENT_TYPES', ())

@deconstructible
class FileValidator(object):
    error_messages = {
        'max_size': ('Ensure this file size (%size) is not greater than %(max_size)s.'),
        'min_size': ('Ensure this file size (%size) is not less than %(min_size)s. '),
        'content_type': 'Files of type %(content_type)s are not supported.',
    }

    def __init__(self, max_size=MAX_SIZE, min_size=MIN_SIZE, content_types=CONTENT_TYPES):
        self.max_size = max_size
        self.min_size = min_size
        self.content_types = content_types

    def __call__(self, data):
        if self.max_size is not None and data.size > self.max_size:
            params = {
                'max_size': filesizeformat(self.max_size),
                'size': filesizeformat(data.size),
            }
            raise ValidationError(self.error_messages['max_size'], 'max_size', params)

        if self.min_size is not None and data.size < self.min_size:
            params = {
                'min_size': filesizeformat(self.mix_size),
                'size': filesizeformat(data.size)
            }
            raise ValidationError(self.error_messages['min_size'], 'min_size', params)

        if self.content_types is not None and len(self.content_types):
            content_type = magic.from_buffer(data.read(), mime=True)
            data.seek(0) # seek to start for future mime checks by django

            if content_type not in self.content_types:
                params = {
                    'content_type': content_type
                }
                raise ValidationError(self.error_messages['content_type'], 'content_type', params)

    def __eq__(self, other):
        return isinstance(other, FileValidator)
