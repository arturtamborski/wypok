from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from . import models

def home(response):
    posts = models.Post.objects.all()
    return render(response, 'excavation/home.html', {'posts': posts})

def post(response, post_id, slug=None):
    post = get_object_or_404(models.Post, id=post_id)
    if slug is None:
        return redirect(post)
    return render(response, 'excavation/post.html', {'post': post})