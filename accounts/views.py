from django.shortcuts import render, get_object_or_404
from django.views import generic
from . import models
import sections


def profile(response, profile):
    profile = models.Profile.objects.get_profile(profile)
    posts   = models.Profile.objects.get_profile_posts(profile)
    return render(response, 'account/profile.html', {'profile': profile, 'posts': posts})
