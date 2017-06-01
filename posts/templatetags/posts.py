from django import template


register = template.Library()

@register.inclusion_tag('posts/snippets/listing.html', takes_context=True)
def render_posts(context, section):
    posts = section.post_set.all()
    return dict(
        request = context.request,
        posts = posts,
    )
