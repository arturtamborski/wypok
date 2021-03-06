from django import template


register = template.Library()

@register.inclusion_tag('posts/snippets/listing.html', takes_context=True)
def posts_listing(context, section):
    posts = section.post_set.select_related('section', 'author').all()

    return dict(
        request = context.request,
        posts = posts,
    )
