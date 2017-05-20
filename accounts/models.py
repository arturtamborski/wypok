from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from sections import models as sections
from wypok.markup import markup


class ProfileQuerySet(models.QuerySet):
    def get_profile(self, username):
        return Profile.objects.get(user__username=username)

    def get_profile_posts(self, username):
        return sections.Post.objects.filter(author__username=username)


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
        (HIDDEN,    'Don\'t show'),
    )

    objects = ProfileQuerySet.as_manager()

    user            = models.OneToOneField(User, unique=True, on_delete=models.CASCADE)
    state           = models.CharField(max_length=1, choices=STATES, default=NOT_ACTIVATED)
    gender          = models.CharField(max_length=1, choices=GENDERS, default=HIDDEN)
    description     = models.TextField(blank=True)
    description_html= models.TextField(editable=False, blank=True)

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        self.description_html = markup(self.description)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('accounts:show', args=[self.user.username])
