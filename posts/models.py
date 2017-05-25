from django.utils.text import slugify
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
from django.db import models

from wypok.markup import markup
from sections.models import Section


class PostQuerySet(models.QuerySet):
    pass


class Post(models.Model):
    class Meta:
        ordering = ('-date',)

    objects = PostQuerySet.as_manager()

    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    title = models.CharField(max_length=256)
    slug = models.SlugField(editable=False)
    link = models.URLField(max_length=256, default='', blank=True)
    date = models.DateTimeField(auto_now_add=True, editable=False)
    content = models.TextField()
    content_html = models.TextField(editable=False, blank=True)

    def __str__(self):
        return self.slug

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        self.content_html = markup(self.content)

        self.full_clean()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('sections:posts:detail', args=[self.section, self.id, self.slug])

    def prettify(self):
        return self.title
