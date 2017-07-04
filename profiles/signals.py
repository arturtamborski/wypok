from allauth.account.signals import email_confirmed
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.signals import user_logged_in
from django.db.models.signals import post_save
from django.conf import settings
from django.utils import timezone
from datetime import timedelta

from profiles.models import Profile


@receiver(post_save, sender=get_user_model())
def profile_create(sender, instance, created, **kwargs):
    user = instance
    if created:
        Profile.objects.create(user=instance)
    user.profile.save()


@receiver(email_confirmed)
def profile_activate_status(email_address, **kwargs):
    profile = Profile.objects.get(user__email=email_address.email)
    profile.state = Profile.GREEN
    profile.save()

    group = Group.objects.get(name='green')
    profile.user.groups.add(group)
    profile.user.save()


@receiver(user_logged_in)
def profile_login(sender, user, request, **kwargs):
    user.profile.update_state()
