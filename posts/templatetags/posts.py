from django import template


register = template.Library()

@register.inclusion_tag('posts/snippets/listing.html')
def render_posts(section):
    posts = section.post_set.all()
    return dict(
        section = section,
        posts = posts,
    )
