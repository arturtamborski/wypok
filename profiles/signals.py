from django.dispatch import receiver
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save

from allauth.account.signals import email_confirmed
from profiles.models import Profile


@receiver(post_save, sender=User)
def profile_create(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


@receiver(email_confirmed)
def profile_activate_status(request, email_address, **kwargs):
    profile = Profile.objects.get(user__email=email_address.email)
    profile.state = Profile.YOUNG
    profile.save()
