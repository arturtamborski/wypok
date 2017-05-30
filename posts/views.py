from allauth.account.decorators import verified_email_required as login_required
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.urls import reverse

from wypok.utils.membership_required import membership_required
from wypok.utils.ownership_required import ownership_required
from sections.models import Section
from posts.models import Post
from posts.forms import PostCreateForm, PostUpdateForm, PostDeleteForm


def redir(request, section, id):
    post = get_object_or_404(Post, id=id)
    return redirect(post)


@ownership_required(Post, raise_exception=False, id='id')
def detail(request, section, id, slug):
    return render(request, 'posts/detail.html', dict(
        post = id,
    ))


def listing(request, section, id, slug):
    posts = get_list_or_404(Post, section=section)

    return render(request, 'posts/listing.html', dict(
        posts = posts,
    ))


@login_required
@membership_required('users')
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
@membership_required('users')
@ownership_required(Post, id='id')
def update(request, section, id, slug):
    post = id

    form = PostUpdateForm(instance=post)
    if request.method == 'POST':
        form = PostUpdateForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save()
            return redirect(post)

    return render(request, 'posts/update.html', dict(
        post = post,
        form = form,
    ))


@login_required
@membership_required('users')
@ownership_required(Post, id='id')
def delete(request, section, id, slug):
    post = id

    form = PostDeleteForm(instance=post)
    if request.method == 'POST':
        form = PostDeleteForm(request.POST, instance=post)
        if form.is_valid():
            section = post.section
            post.delete()
            return redirect('sections:detail', section)

    return render(request, 'posts/delete.html', dict(
        post = post,
        form = form,
    ))
