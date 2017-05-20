from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from allauth.account.signals import email_confirmed
from . import models

@receiver(post_save, sender=User)
def profile_create(sender, instance, created, **kwargs):
    if created:
        models.Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def profile_save(sender, instance, **kwargs):
    instance.profile.save()

@receiver(email_confirmed)
def profile_activate_status(request, email_address, **kwargs):
    profile = models.Profile.objects.get(user__email=email_address.email)
    profile.state = models.Profile.YOUNG
    profile.save()
