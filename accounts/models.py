from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

class Profile(models.Model):
    user = models.OneToOneField(User, unique=True, on_delete=models.CASCADE)

    NOT_ACTIVATED   = 'N'
    ACTIVATED       = 'A'
    DELETED         = 'D'
    BANNED          = 'B'

    STATES = (
        (NOT_ACTIVATED, 'Not activated'),
        (ACTIVATED,     'Activated'),
        (DELETED,       'Deleted'),
        (BANNED,        'Banned'),
    )

    state = models.CharField(
        max_length=1,
        choices=STATES,
        default=NOT_ACTIVATED,
    )

    description = models.TextField(
        blank=True,
    )

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('accounts:profile', args=[self.user.username])
