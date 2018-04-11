from django.shortcuts import render, redirect

from . import forms
from . import models


def index(request):
    return render(request, 'tags/index.html', dict(
        tags = models.Tag.objects.get_all(request.user)
    ))


def show(request, tag):
    return render(request, 'tags/show.html', dict(
        tag = models.Tag.objects.get_one(tag, request.user)
    ))


def create(request):
    form = forms.TagCreate()

    if request.method == 'POST':
        form = forms.TagCreate(request.POST, request.FILES)
        if form.is_valid():
            tag = form.save(commit=False)
            tag.author = request.user
            tag.save()
            return redirect(tag)

    return render(request, 'tags/create.html', dict(
        form = form,
    ))


def update(request, tag):
    tag = models.Tag.get_object(tag, request.user)
    form = TagUpdate(instance=tag)

    if request.method == 'POST':
        form = TagUpdate(request.POST, request.FILES, instance=tag)
        if form.is_valid():
            tag = form.save()
            return redirect(tag)

    return render(request, 'tags/update.html', dict(
        tag = tag,
        form = form,
    ))


def delete(request, tag):
    tag = models.Tag.get_object(tag, request.user)
    form = forms.TagDelete(instance=tag)

    if request.method == 'POST':
        form = forms.TagDelete(request.POST, instance=tag)
        if form.is_valid():
            tag.delete()
            return redirect('tags:index')

    return render(request, 'tags/delete.html', dict(
        tag = tag,
        form = form,
    ))
