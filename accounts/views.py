from allauth.account.decorators import verified_email_required as login_required
from django.shortcuts import redirect, render
from django.views import generic
from . import models
from . import forms
import sections


def show(request, profile):
    profile = models.Profile.objects.get_profile(profile)
    posts   = models.Profile.objects.get_profile_posts(profile)
    return render(request, 'accounts/show.html', {'profile': profile, 'posts': posts})


@login_required
def edit(request, profile):
    profile = models.Profile.objects.get_profile(profile)
    posts   = models.Profile.objects.get_profile_posts(profile)

    if str(profile) != str(request.user):
        return redirect(profile)

    form = forms.ProfileForm(instance=profile)
    if request.method == 'POST':
        form = forms.ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            post = form.save()
            return redirect(profile)

    return render(request, 'accounts/edit.html', {'profile': profile, 'form': form})
