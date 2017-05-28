from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.conf import settings

from allauth.account.signals import email_confirmed
from profiles.models import Profile


DEFAULT_USER_GROUP = getattr(settings, 'DEFAULT_USER_GROUP', 'users')

@receiver(post_save, sender=get_user_model())
def profile_create(sender, instance, created, **kwargs):
    user = instance
    if created:
        Profile.objects.create(user=user)
    user.profile.save()


@receiver(email_confirmed)
def profile_activate_status(email_address, **kwargs):
    profile = Profile.objects.get(user__email=email_address.email)
    profile.state = Profile.YOUNG
    group = Group.objects.get(name=DEFAULT_USER_GROUP)
    profile.user.groups.add(group)
    profile.save()
