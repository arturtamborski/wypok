from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.conf import settings

from wypok.validators import FileValidator
from wypok.utils.markup import markup
from sections.models import Section


PROFILES_IS_OLD_AFTER = getattr(settings, 'PROFILES_IS_OLD_AFTER', 30)

def profiles_avatar_path(instance, filename):
    return settings.PROFILES_AVATAR_PATH.format(id=instance.id, name=filename)


class ProfileQuerySet(models.QuerySet):
    pass


class Profile(models.Model):
    INACTIVE    = 'I'
    GREEN       = 'G'
    ORANGE      = 'O'
    RED         = 'R'
    DELETED     = 'D'
    BANNED      = 'B'

    STATES = (
        (INACTIVE,  'inactive'),
        (GREEN,     'green'),
        (ORANGE,    'orange'),
        (RED,       'red'),
        (DELETED,   'deleted'),
        (BANNED,    'banned'),
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
    state = models.CharField(max_length=1, choices=STATES, default=INACTIVE)
    gender = models.CharField(max_length=1, choices=GENDERS, default=HIDDEN)
    description = models.TextField(blank=True)
    description_html = models.TextField(editable=False, blank=True)
    avatar = models.FileField(max_length=256, blank=True, null=True,
        upload_to=profiles_avatar_path, default=settings.PROFILES_DEFAULT_AVATAR,
        validators=[FileValidator(content_types=settings.PROFILES_ALLOWED_CONTENT_TYPES)])

    def save(self, *args, **kwargs):
        self.description_html = markup(self.description)
        self.update_state()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.username

    def prettify(self):
        return '@%s' % self.user.username

    def get_owner(self):
        return self.user

    def get_absolute_url(self):
        return reverse('profiles:detail', args=[self.user.username])

    def update_state(self):
        for state in self.STATES:
            if self.user.groups.filter(name=state[1]).exists():
                self.state = state[0]

        if self.user.profile == self.GREEN:
            if (timezone.now() - self.user.date_joined).days > PROFILES_IS_OLD_AFTER:
                group = Group.objects.get(name='orange')
                self.user.groups.add(group)
                self.user.save()
                self.user.profile.state = Profile.ORANGE
                self.user.profile.save()
