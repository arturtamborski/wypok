from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save

from allauth.account.signals import email_confirmed
from profiles.models import Profile


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
    profile.save()
