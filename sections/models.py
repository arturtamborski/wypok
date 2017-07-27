from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils.text import slugify

from wypok.validators import FileValidator
from wypok.utils.markup import markup
from sections.validators import section_name_validator


def sections_background_path(instance, filename):
    return settings.SECTIONS_BACKGROUND_PATH.format(id=instance.id, name=filename)

class SectionQuerySet(models.QuerySet):
    pass


class Section(models.Model):
    objects = SectionQuerySet.as_manager()

    admin = models.ForeignKey(get_user_model(), default='1')
    name = models.SlugField(max_length=20, validators=[section_name_validator])
    description = models.TextField()
    description_html = models.TextField(editable=False, blank=True)
    background = models.FileField(max_length=256, blank=True, null=True,
        upload_to=sections_background_path, default=settings.SECTIONS_DEFAULT_BACKGROUND,
        validators=[FileValidator(content_types=settings.SECTIONS_ALLOWED_CONTENT_TYPES)])

    def save(self, *args, **kwargs):
        self.name = slugify(self.name)
        self.description_html = markup(self.description)

        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def prettify(self):
        return '/%s/' % self.name

    def get_owner(self):
        return self.admin

    def get_absolute_url(self):
        return reverse('sections:detail', args=[self.name])
