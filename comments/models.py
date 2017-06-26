from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
from django.db import models
from django.conf import settings
from os import path

from wypok.validators import FileValidator
from wypok.utils.markup import markup
from posts.models import Post

def comments_attachment_path(instance, filename):
    return settings.COMMENTS_ATTACHMENT_PATH.format(id=instance.pk, name=filename)


class CommentQuerySet(models.QuerySet):
    pass


class Comment(models.Model):
    class Meta:
        ordering = ('posted',)

    objects = CommentQuerySet.as_manager()

    author = models.ForeignKey(get_user_model())
    post = models.ForeignKey(Post)
    parent = models.ForeignKey('Comment', null=True, blank=True)
    posted = models.DateTimeField(auto_now_add=True, editable=False)
    content = models.TextField(blank=True)
    content_html = models.TextField(editable=False, blank=True)
    attachment = models.FileField(max_length=256, blank=True, null=True,
        upload_to=comments_attachment_path,
        validators=[FileValidator(content_types=settings.COMMENTS_ALLOWED_CONTENT_TYPES)])

    def save(self, *args, **kwargs):
        self.content_html = markup(self.content)

        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.id)

    def prettify(self):
        return '#%s' % self.id

    def get_owner(self):
        return self.author

    def get_absolute_url(self):
        return reverse('sections:posts:comments:detail', args=[self.post.section, self.post.id, self.post.slug, self.id])
