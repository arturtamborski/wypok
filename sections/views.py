from django.views.decorators.cache import cache_page
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from . import models
from . import forms

@cache_page(settings.CACHE_TTL)
def home(request, section=None):
    if section is None:
        return redirect('sections:home', 'all')

    section = models.Section.objects.get_section(section)
    posts   = models.Post.objects.get_posts(section)
    return render(request, 'sections/home.html', {'section': section, 'posts': posts})

def new_post(request, section):
    form = forms.PostForm()
    if request.method == 'POST':
        form = forms.PostForm(request.POST)
        if form.is_valid():
            pass

    return render(request, 'sections/new_post.html', {'form': form})

@cache_page(settings.CACHE_TTL)
def post(request, section, id, slug=None):
    section = models.Section.objects.get_section(section)
    post    = models.Post.objects.get_post(id)
    if slug is None:
        return redirect(post)
    return render(request, 'sections/post.html', {'section': section, 'post': post})
