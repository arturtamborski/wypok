from django import template
from django.conf import settings

from wypok.utils import membership_required


register = template.Library()


@register.filter
def is_member(user, group):
    return membership_required.is_member(user, group)
