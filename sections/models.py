from django.utils.text import slugify
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
from django.db import models

from wypok.markup import markup
from sections.validators import section_name_validator
from django.core.validators import RegexValidator


class SectionQuerySet(models.QuerySet):
    pass


class Section(models.Model):
    objects = SectionQuerySet.as_manager()

    admin = models.ForeignKey(get_user_model(), default='1')
    name = models.SlugField(max_length=20, validators=[section_name_validator])
    description = models.TextField()
    description_html = models.TextField(editable=False, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = slugify(self.name)
        self.description_html = markup(self.description)

        self.full_clean()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('sections:detail', args=[self.name])

    def prettify(self):
        return '/%s/' % self.name

    def is_owner(self, request):
        return self.admin == request.user
