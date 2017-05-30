from allauth.account.decorators import verified_email_required as login_required
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.urls import reverse

from wypok.utils.membership_required import membership_required
from wypok.utils.ownership_required import ownership_required
from sections.models import Section
from posts.models import Post
from comments.models import Comment
from comments.forms import CommentCreateForm, CommentUpdateForm, CommentDeleteForm


def detail(request, section, id, slug, comment):
    return redirect(
        reverse('sections:posts:comments:listing', args=[section, id, slug]) + '#' + comment
    )


def listing(request, section, id, slug):
    comments = get_list_or_404(Comment, post=id)

    return render(request, 'comments/listing.html', dict(
        comments = comments,
    ))


@login_required
@membership_required('users')
@ownership_required(Post, raise_exception=False, id='id')
def create(request, section, id, slug):
    form = CommentCreateForm()

    if request.method == 'POST':
        form = CommentCreateForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect(comment)

    return render(request, 'comments/create.html', dict(
        post = post,
        form = form,
    ))


@login_required
@membership_required('users')
@ownership_required(Comment, id='comment')
def update(request, section, id, slug, comment):
    form = CommentUpdateForm(instance=comment)

    if request.method == 'POST':
        form = CommentUpdateForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save()
            return redirect(comment)

    return render(request, 'comments/update.html', dict(
        comment = comment,
        form = form,
    ))


@login_required
@membership_required('users')
@ownership_required(Comment, id='comment')
def delete(request, section, id, slug, comment):

    form = CommentDeleteForm(instance=comment)
    if request.method == 'POST':
        form = CommentDeleteForm(request.POST, instance=comment)
        if form.is_valid():
            post = comment.post
            comment.delete()
            return redirect(post)

    return render(request, 'comments/delete.html', dict(
        comment = comment,
        form = form,
    ))
