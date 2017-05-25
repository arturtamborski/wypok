from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model

from wypok.markup import markup
from sections.models import Section


class ProfileQuerySet(models.QuerySet):
    pass


class Profile(models.Model):

    NOT_ACTIVATED   = 'N'
    YOUNG           = 'Y'
    OLD             = 'O'
    DELETED         = 'D'
    BANNED          = 'B'

    STATES = (
        (NOT_ACTIVATED, 'Not activated'),
        (YOUNG,         'Young'),
        (OLD,           'Old'),
        (DELETED,       'Deleted'),
        (BANNED,        'Banned'),
    )

    MALE    = 'M'
    FEMALE  = 'F'
    HIDDEN  = 'H'

    GENDERS = (
        (MALE,      'Male'),
        (FEMALE,    'Female'),
        (HIDDEN,    'Hidden'),
    )

    objects = ProfileQuerySet.as_manager()

    user = models.OneToOneField(get_user_model(), unique=True, on_delete=models.CASCADE)
    state = models.CharField(max_length=1, choices=STATES, default=NOT_ACTIVATED)
    gender = models.CharField(max_length=1, choices=GENDERS, default=HIDDEN)
    description = models.TextField(blank=True)
    description_html = models.TextField(editable=False, blank=True)

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        self.description_html = markup(self.description)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('profiles:detail', args=[self.user.username])

    def prettify(self):
        return '@%s' % self.user.username
