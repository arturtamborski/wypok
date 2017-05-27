from functools import wraps

from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from django.conf import settings


OWNERSHIP_REQUIRED_CALLABLE = getattr(settings, 'OWNERSHIP_REQUIRED_CALLABLE', 'is_owner')

def ownership_required(model):
    def decorator(func):
        def view(request, *args, **kwargs):
            if hasattr(model, OWNERSHIP_REQUIRED_CALLABLE):
                attr = getattr(model, OWNERSHIP_REQUIRED_CALLABLE)
                if attr(model, request, **kwargs):
                    return func(request, *args, **kwargs)
                raise PermissionDenied
            raise ImproperlyConfigured('Provided model "%s" doesn\'t have requried callable for checking ownership.' % model.__name__)
        return wraps(func)(view)
    return decorator
