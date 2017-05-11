from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from . import models

def home(response, section=None):
    if section is None:
        return redirect('sections:home', 'all')

    posts = models.Post.objects.filter(section__slug=section).order_by('-date')
    return render(response, 'sections/home.html', {'posts': posts})

def post(response, section, id, slug=None):
    post = get_object_or_404(models.Post, section__slug=section, id=id)
    if slug is None:
        return redirect(post)
    return render(response, 'sections/post.html', {'post': post})
