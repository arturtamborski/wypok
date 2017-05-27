from django import template
from django.conf import settings


PRETTIFY_CALLABLE = getattr(settings, 'PRETTIFY_CALLABLE', 'prettify')

register = template.Library()

@register.filter
def prettify(obj):
    if hasattr(obj, PRETTIFY_CALLABLE):
        attr = getattr(obj, PRETTIFY_CALLABLE)
        if callable(attr):
            return attr()
        return attr
    return obj
