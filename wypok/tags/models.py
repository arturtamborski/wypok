from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model

from wypok.utils.markup import markup

from . import settings
from . import managers
from . import validators


def background_path(instance, filename):
    return settings.BACKGROUND_PATH.format(id=instance.id, name=filename)


class Tag(models.Model):
    objects = managers.TagQuerySet.as_manager()

    author = models.ForeignKey(
        to = get_user_model(),
        on_delete = models.PROTECT
    )

    name = models.SlugField(
        max_length = settings.MAX_LENGTH,
        allow_unicode = True, # experimental
        validators = [validators.name_validator]
    )

    description = models.TextField(
        blank = False
    )

    description_html = models.TextField(
        editable = False,
        blank = True
    )

    background = models.FileField(
        upload_to=background_path,
        max_length=256,
        blank=True,
        null=True,
        default=settings.DEFAULT_BACKGROUND,
        validators=[validators.background_validator]
    )

    def __str__(self):
        return self.name

    def prettify(self):
        return '#%s' % self.name

    def get_owner(self):
        return self.author

    def save(self, *args, **kwargs):
        self.description_html = markup(self.description)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('tags:show', args=[self.name])
