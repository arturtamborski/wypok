from allauth.account.decorators import verified_email_required as login_required
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponseNotFound, Http404
from wypok.cache import mark_for_caching
from . import models
from . import forms

def check_section(section):
    if not models.Section.objects.section_exists(section):
        raise Http404


@mark_for_caching
def home(request, section=None):
    if section is None:
        return redirect('sections:home', 'all')
    check_section(section)

    section = models.Section.objects.get_section(section)
    posts   = models.Post.objects.get_posts(section)
    return render(request, 'sections/home.html', {'section': section, 'posts': posts})


@mark_for_caching
def post(request, section, id, slug=None):
    check_section(section)

    section = models.Section.objects.get_section(section)
    post    = models.Post.objects.get_post(id)
    if slug is None:
        return redirect(post)
    return render(request, 'sections/post.html', {'section': section, 'post': post})


@login_required
def new_post(request, section):
    check_section(section)

    form = forms.PostForm()
    if request.method == 'POST':
        form = forms.PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.section = models.Section.objects.get_section(section)
            post.save()
            return redirect(post)

    return render(request, 'sections/new_post.html', {'section': section, 'form': form})


@login_required
def edit_post(request, section, id, slug=None):
    check_section(section)

    section = models.Section.objects.get_section(section)
    post    = models.Post.objects.get_post(id)
    if slug is None:
        return redirect('sections:edit_post', kwargs={'section': section, 'id': id, 'slug': post.slug})

    form = forms.PostForm(instance=post)
    if request.method == 'POST':
        form = forms.PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save()
            return redirect(post)

    return render(request, 'sections/edit_post.html', {'section': section, 'post': post, 'form': form})
