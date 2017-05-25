from allauth.account.decorators import verified_email_required as login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.urls import reverse

from profiles.models import Profile
from profiles.forms import ProfileUpdateForm, ProfileDeleteForm


def detail(request, profile):
    profile = get_object_or_404(Profile, user__username=profile)

    return render(request, 'profiles/detail.html', dict(
        profile = profile,
    ))


@login_required
def update(request, profile):
    profile = get_object_or_404(Profile, user__username=profile)
    form = ProfileUpdateForm(instance=profile)

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=profile)
        if form.is_valid():
            post = form.save()
            return redirect(profile)

    return render(request, 'profiles/update.html', dict(
        profile = profile,
        form = form,
    ))


@login_required
def delete(request, profile):
    profile = get_object_or_404(Profile, user__username=profile)
    user = get_object_or_404(get_user_model(), username=profile)

    form = ProfileDeleteForm(instance=profile)
    if request.method == 'POST':
        form = ProfileDeleteForm(request.POST, instance=profile)
        if form.is_valid():
            profile.delete()
            user.delete()
            return redirect('sections:home')

    return render(request, 'profiles/delete.html', dict(
        profile = profile,
        form = form,
    ))
