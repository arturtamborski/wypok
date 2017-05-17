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

@login_required
@mark_for_caching
def new_post(request, section):
    check_section(section)

    form = forms.PostForm()
    if request.method == 'POST':
        form = forms.PostForm(request.POST)
        if form.is_valid():
            pass

    return render(request, 'sections/new_post.html', {'form': form})

@mark_for_caching
def post(request, section, id, slug=None):
    check_section(section)

    section = models.Section.objects.get_section(section)
    post    = models.Post.objects.get_post(id)
    if slug is None:
        return redirect(post)
    return render(request, 'sections/post.html', {'section': section, 'post': post})
