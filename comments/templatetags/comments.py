from django import template

from comments.forms import CommentCreateForm


register = template.Library()

@register.inclusion_tag('comments/snippets/listing.html', takes_context=True)
def comments_listing(context, post):
    comments = post.comment_set.all()
    return dict(
        request = context.request,
        comments = comments,
    )


@register.inclusion_tag('comments/snippets/create.html')
def comments_create(post):
    return dict(
        post = post,
        form = CommentCreateForm(),
    )
