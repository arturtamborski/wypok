from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.db import models


class Post(models.Model):
    author  = models.ForeignKey(User, on_delete=models.CASCADE)
    title   = models.CharField(max_length=256)
    slug    = models.SlugField(editable=False)
    date    = models.DateTimeField(default=timezone.now, editable=False)
    content = models.TextField()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('excavation:post', args=[self.id, self.slug])
