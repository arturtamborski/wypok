from django.db import models
from django.utils.text import slugify
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.db import models


class Section(models.Model):
    admin   = models.ForeignKey(User, on_delete=models.CASCADE)
    title   = models.CharField(max_length=128)
    slug    = models.SlugField(max_length=64)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('sections:home', args=[self.slug])



class Post(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    author  = models.ForeignKey(User, on_delete=models.CASCADE)
    title   = models.CharField(max_length=256)
    slug    = models.SlugField(editable=False)
    link    = models.URLField(max_length=256, default='', blank=True)
    date    = models.DateTimeField(auto_now_add=True, editable=False)
    content = models.TextField()
    content_html = models.TextField(editable=False, blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)

        # im saving here two times, because get_absolute_url needs id
        # and if this model is saved for first time, then id is empty
        super().save(*args, **kwargs)
        if not self.link:
            self.link = self.get_absolute_url()

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('sections:post', args=[self.section.slug, self.id, self.slug])
