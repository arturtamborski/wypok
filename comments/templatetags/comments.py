from django import template

from comments.forms import CommentCreateForm


register = template.Library()

@register.inclusion_tag('comments/snippets/listing.html')
def render_comments(post):
    comments = post.comment_set.all()
    return dict(
        comments = comments,
    )


@register.inclusion_tag('comments/snippets/create.html')
def render_comments_create(post):
    return dict(
        post = post,
        form = CommentCreateForm(),
    )
