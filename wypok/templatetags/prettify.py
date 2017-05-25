from django import template


PRETTIFY_CALLABLE = 'prettify'


register = template.Library()

@register.filter
def prettify(obj):
    if hasattr(obj, PRETTIFY_CALLABLE):
        attr = getattr(obj, PRETTIFY_CALLABLE)
        if callable(attr):
            return attr()
        return attr
    return obj
