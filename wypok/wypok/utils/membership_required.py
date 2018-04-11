from functools import wraps

from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from django.conf import settings


MEMBERSHIP_REQUIRED_PASS_RESULT = getattr(settings, 'MEMBERSHIP_REQUIRED_PASS_RESULT', True)
MEMBERSHIP_REQUIRED_RESULT_NAME = getattr(settings, 'MEMBERSHIP_REQUIRED_RESULT_NAME', 'is_member')


def is_member(user, group):
    return user.groups.filter(name=group).exists() or user.is_superuser


def membership_required(group, raise_exception=True):
    def decorator(func):
        def view(request, *args, **kwargs):
            result = is_member(request.user, group)

            if not result and raise_exception:
                raise PermissionDenied

            if MEMBERSHIP_REQUIRED_PASS_RESULT:
                setattr(request, MEMBERSHIP_REQUIRED_RESULT_NAME, result)

            return func(request, *args, **kwargs)
        return wraps(func)(view)
    return decorator
