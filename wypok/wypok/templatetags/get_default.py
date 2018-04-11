from os import path

from django import template
from django.conf import settings


register = template.Library()


@register.filter
def get_default(model, field):
    return model._meta.get_field(field).get_default()
