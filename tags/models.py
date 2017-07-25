from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model

from wypok.utils.markup import markup
from tags.validators import tag_name_validator


class TagQuerySet(models.QuerySet):
    pass


class Tag(models.Model):
    author = models.ForeignKey(get_user_model(), default='1')
    name = models.SlugField(max_length=64, validators=[tag_name_validator])
    description = models.TextField()
    description_html = models.TextField(editable=False, blank=True)

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
