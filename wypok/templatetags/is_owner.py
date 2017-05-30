from django import template
from django.conf import settings

from wypok.utils import ownership_required

register = template.Library()

@register.filter
def is_owner(user, obj):
    return ownership_required.is_owner(user, obj)
