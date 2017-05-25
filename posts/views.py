from allauth.account.decorators import verified_email_required as login_required
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.urls import reverse

from sections.models import Section
from posts.models import Post
from posts.forms import PostCreateForm, PostUpdateForm, PostDeleteForm


def redir(request, section, id):
    post = get_object_or_404(Post, id=id)
    return redirect(post)


def detail(request, section, id, slug):
    section = get_object_or_404(Section, name=section)
    post = get_object_or_404(Post, id=id)

    return render(request, 'posts/detail.html', dict(
        section = section,
        post = post,
    ))


def listing(request, section, id, slug):
    section = get_object_or_404(Section, name=section)
    posts = get_list_or_404(Post, section=section)

    return render(request, 'posts/listing.html', dict(
        section = section,
        posts = posts,
    ))


def create(request, section):
    section = get_object_or_404(Section, name=section)

    form = PostCreateForm()
    if request.method == 'POST':
        form = PostCreateForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.section = section
            post.save()
            return redirect(post)

    return render(request, 'posts/create.html', dict(
        section = section,
        form = form,
    ))


@login_required
def update(request, section, id, slug):
    section = get_object_or_404(Section, name=section)
    post = get_object_or_404(Post, id=id)

    form = PostUpdateForm(instance=post)
    if request.method == 'POST':
        form = PostUpdateForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.section = section
            post.save()
            return redirect(post)

    return render(request, 'posts/update.html', dict(
        section = section,
        post = post,
        form = form,
    ))


@login_required
def delete(request, section, id, slug):
    section = get_object_or_404(Section, name=section)
    post = get_object_or_404(Post, id=id)

    form = PostDeleteForm(instance=post)
    if request.method == 'POST':
        form = PostDeleteForm(request.POST, instance=post)
        if form.is_valid():
            post.delete()
            return redirect('sections:detail', section)

    return render(request, 'posts/delete.html', dict(
        section = section,
        post = post,
        form = form,
    ))
