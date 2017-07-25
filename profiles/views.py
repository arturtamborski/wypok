from allauth.account.decorators import verified_email_required as login_required
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.conf import settings

from wypok.utils.membership_required import membership_required
from wypok.utils.ownership_required import ownership_required
from profiles.models import Profile
from profiles.forms import ProfileUpdateForm, ProfileDeleteForm


@ownership_required(Profile, raise_exception=False, user__username='profile')
def detail(request, profile):
    return render(request, 'profiles/detail.html', dict(
        profile = profile,
    ))


def listing(request):
    profiles = get_list_or_404(Profile)

    return render(request, 'profiles/listing.html', dict(
        profiles = profiles,
    ))


@login_required
@membership_required('green')
@ownership_required(Profile, user__username='profile')
def update(request, profile):
    form = ProfileUpdateForm(instance=profile)

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile = form.save()
            return redirect(profile)

    return render(request, 'profiles/update.html', dict(
        profile = profile,
        form = form,
    ))


@login_required
@membership_required('green')
@ownership_required(Profile, user__username='profile')
def delete(request, profile):
    form = ProfileDeleteForm(instance=profile)

    if request.method == 'POST':
        form = ProfileDeleteForm(request.POST, instance=profile)
        if form.is_valid():
            user = profile.user
            profile.delete()
            user.delete()
            return redirect('sections:home')

    return render(request, 'profiles/delete.html', dict(
        profile = profile,
        form = form,
    ))
