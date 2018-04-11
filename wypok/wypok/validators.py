from django.conf import settings
from django.core.exceptions import ValidationError
from django.template.defaultfilters import filesizeformat
from django.utils.deconstruct import deconstructible

import magic


MAX_SIZE = getattr(settings, 'FILE_UPLOAD_MAX_MEMORY_SIZE', 2621440) # 2.MB
MIN_SIZE = getattr(settings, 'FILE_UPLOAD_MIN_MEMORY_SIZE', 1024) # 1.KB
CONTENT_TYPES = getattr(settings, 'ALLOWED_CONTENT_TYPES', ())


@deconstructible
class FileValidator(object):
    error_messages = dict(
        max_size = 'Ensure this file size %(size) is not greater than %(max_size)s.',
        min_size = 'Ensure this file size %(size) is not less than %(min_size)s. ',
        content_type = 'Files of type %(content_type)s are not supported.',
    )

    def __init__(self, max_size=MAX_SIZE, min_size=MIN_SIZE, content_types=CONTENT_TYPES):
        self.max_size = max_size
        self.min_size = min_size
        self.content_types = content_types

    def __call__(self, data):
        if self.max_size is not None and data.size > self.max_size:
            raise ValidationError(self.error_messages['max_size'], 'max_size', dict(
                max_size = filesizeformat(self.max_size),
                size = filesizeformat(data.size)
            ))

        if self.min_size is not None and data.size < self.min_size:
            raise ValidationError(self.error_messages['min_size'], 'min_size', dict(
                min_size = filesizeformat(self.mix_size),
                size = filesizeformat(data.size)
            ))

        if self.content_types is not None and len(self.content_types):
            content_type = magic.from_buffer(data.read(), mime=True)
            
            # seek to start for future mime checks by django
            data.seek(0)

            if content_type not in self.content_types:
                raise ValidationError(self.error_messages['content_type'], 'content_type', dict(
                    content_type = content_type
                ))

    def __eq__(self, other):
        return isinstance(other, FileValidator)
