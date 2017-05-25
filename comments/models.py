from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
from django.db import models

from posts.models import Post
from wypok.markup import markup


class CommentQuerySet(models.QuerySet):
    pass


class Comment(models.Model):
    objects = CommentQuerySet.as_manager()

    author = models.ForeignKey(get_user_model())
    post = models.ForeignKey(Post)
    parent = models.ForeignKey('Comment', null=True, blank=True)
    posted = models.DateTimeField(auto_now_add=True, editable=False)
    content = models.TextField()
    content_html = models.TextField(editable=False, blank=True)

    class Meta:
        ordering = ('-posted',)

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        self.content_html = markup(self.content)

        self.full_clean()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('sections:posts:comments:detail', args=[self.post.section, self.post.id, self.post.slug, self.id])

    def prettify(self):
        return '#%s' % self.id
