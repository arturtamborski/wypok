from allauth.account.decorators import verified_email_required as login_required
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.conf import settings

from wypok.utils.membership_required import membership_required
from wypok.utils.ownership_required import ownership_required
from tags.models import Tag
from tags.forms import TagCreateForm, TagUpdateForm, TagDeleteForm


@ownership_required(Tag, raise_exception=False, name='tag')
def detail(request, tag):
    return render(request, 'tags/detail.html', dict(
        tag = tag,
    ))


def listing(request):
    tags = get_list_or_404(Tag)

    return render(request, 'tags/listing.html', dict(
        tags = tags,
    ))


@login_required
@membership_required('green')
def create(request):
    form = TagCreateForm()

    if request.method == 'POST':
        form = TagCreateForm(request.POST, request.FILES)
        if form.is_valid():
            tag = form.save(commit=False)
            tag.author = request.user
            tag.save()
            return redirect(tag)

    return render(request, 'tags/create.html', dict(
        form = form,
    ))


@login_required
@membership_required('green')
@ownership_required(Tag, name='tag')
def update(request, tag):
    form = TagUpdateForm(instance=tag)

    if request.method == 'POST':
        form = TagUpdateForm(request.POST, request.FILES, instance=tag)
        if form.is_valid():
            tag = form.save()
            return redirect(tag)

    return render(request, 'tags/update.html', dict(
        tag = tag,
        form = form,
    ))


@login_required
@membership_required('green')
@ownership_required(Tag, name='tag')
def delete(request, tag):
    form = TagDeleteForm(instance=tag)

    if request.method == 'POST':
        form = TagDeleteForm(request.POST, instance=tag)
        if form.is_valid():
            tag.delete()
            return redirect('home')

    return render(request, 'tags/delete.html', dict(
        tag = tag,
        form = form,
    ))

