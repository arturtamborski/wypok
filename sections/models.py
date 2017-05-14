from django.db import models
from django.utils.text import slugify
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.db import models
from wypok.markup import markup


class SectionQuerySet(models.QuerySet):
    def get_section(self, name):
        return Section.objects.get(name=name)


class Section(models.Model):
    objects = SectionQuerySet.as_manager()

    admin   = models.ForeignKey(User, on_delete=models.CASCADE)
    name    = models.SlugField(max_length=64)
    description     = models.TextField()
    description_html= models.TextField(editable=False, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.description_html = markup(self.description)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('sections:home', args=[self.name])


class PostQuerySet(models.QuerySet):
    def get_post(self, id):
        return Post.objects.get(id=id)

    def get_posts(self, section):
        return Post.objects.filter(section__name=section).order_by('-date')

class Post(models.Model):
    objects = PostQuerySet.as_manager()

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
        self.content_html = markup(self.content)

        # im saving here two times, because get_absolute_url needs id
        # and if this model is saved for first time then id is empty
        super().save(*args, **kwargs)
        if not self.link:
            self.link = self.get_absolute_url()

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('sections:post', args=[self.section, self.id, self.slug])
