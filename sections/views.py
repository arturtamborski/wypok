from django.views.decorators.cache import cache_page
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from . import models

@cache_page(settings.CACHE_TTL)
def home(response, section=None):
    if section is None:
        return redirect('sections:home', 'all')

    section = models.Section.objects.get_section(section)
    posts   = models.Post.objects.get_posts(section)
    return render(response, 'sections/home.html', {'section': section, 'posts': posts})

@cache_page(settings.CACHE_TTL)
def post(response, section, id, slug=None):
    section = models.Section.objects.get_section(section)
    post    = models.Post.objects.get_post(id)
    if slug is None:
        return redirect(post)
    return render(response, 'sections/post.html', {'section': section, 'post': post})
