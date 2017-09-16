from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
from django.db import models
from django.conf import settings

from wypok.validators import FileValidator
from wypok.utils.markup import markup
from wypok.utils.slugify import slugify_max
from sections.models import Section


def posts_attachment_path(instance, filename):
    return settings.POSTS_ATTACHMENT_PATH.format(id=instance.id, name=filename)


class PostQuerySet(models.QuerySet):
    pass


class Post(models.Model):
    class Meta:
        ordering = ('-date',)

    objects = PostQuerySet.as_manager()

    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    title = models.CharField(max_length=256)
    slug = models.SlugField(max_length=32, editable=False)
    link = models.URLField(max_length=256, default='', blank=True)
    date = models.DateTimeField(auto_now_add=True, editable=False)
    content = models.TextField(blank=True)
    content_html = models.TextField(editable=False, blank=True)
    attachment = models.FileField(max_length=256, blank=True, null=True,
        upload_to=posts_attachment_path,
        validators=[FileValidator(content_types=settings.POSTS_ALLOWED_CONTENT_TYPES)])

    def save(self, *args, **kwargs):
        self.slug = slugify_max(self.title, 32)
        self.content_html = markup(self.content)

        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.slug

    def prettify(self):
        return self.title

    def get_owner(self):
        return self.author

    def get_absolute_url(self):
        return reverse('sections:posts:detail', args=[self.section, self.id, self.slug])

