from django.db import models
from django.utils import timezone

from . import validators

class Account(models.Model):

    NOT_ACTIVATED   = 'N'
    ACTIVATED       = 'A'
    DELETED         = 'D'
    BANNED          = 'B'

    STATES = (
        (NOT_ACTIVATED,     'Not activated'),
        (ACTIVATED,         'Activated'),
        (DELETED,           'Deleted'),
        (BANNED,            'Banned'),
    )

    state = models.CharField(
        max_length=1,
        choices=STATES,
        default=NOT_ACTIVATED,
    )

    name = models.CharField(
        max_length=20,
        unique=True,
        validators=[validators.AccountNameValidator],
    )

    email = models.EmailField(
        max_length=200,
    )

    description = models.TextField(
        blank=True,
    )

    created = models.DateTimeField(
        editable=False,
        default=timezone.now,
    )

    USERNAME_FIELD  = 'name'
    REQUIRED_FIELDS = [
        'email',
    ]

    class Meta:
        swappable = 'AUTH_USER_MODEL'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('user:profile', args=(self.name))

    #def is_not_activated(self):
    #    return self.state[0] == NOT_ACTIVATED

    #def is_activated(self):
    #    return self.state[0] == ACTIVATED

    #def is_deleted(self):
    #    return self.state[0] == DELETED

    #def is_banned(self):
    #    return self.state[0] == BANNED

    #def check(self, **kwargs):
    #    errors = super().check(**kwargs)
    #    errors.extend(self._check_name)
    #    return errors

    #def _check_name(self):
    #    return NAME_REGEX.match(self.name) is not None
