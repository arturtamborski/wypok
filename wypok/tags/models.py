from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.conf import settings

from wypok.validators import FileValidator
from wypok.utils.markup import markup
from tags.validators import tag_name_validator


def tags_background_path(instance, filename):
    return settings.TAGS_BACKGROUND_PATH.format(id=instance.id, name=filename)


class TagQuerySet(models.QuerySet):
    pass


class Tag(models.Model):
    author = models.ForeignKey(get_user_model(), default='1', on_delete=models.PROTECT)
    name = models.SlugField(max_length=64, validators=[tag_name_validator])
    description = models.TextField()
    description_html = models.TextField(editable=False, blank=True)
    background = models.FileField(max_length=256, blank=True, null=True,
        upload_to=tags_background_path, default=settings.TAGS_DEFAULT_BACKGROUND,
        validators=[FileValidator(content_types=settings.TAGS_ALLOWED_CONTENT_TYPES)])

    def save(self, *args, **kwargs):
        self.description_html = markup(self.description)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def prettify(self):
        return '#%s' % self.name

    def get_owner(self):
        return self.author

    def get_absolute_url(self):
        return reverse('tags:detail', args=[self.name])
