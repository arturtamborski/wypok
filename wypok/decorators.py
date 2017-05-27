from functools import wraps

from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from django.shortcuts import get_object_or_404
from django.conf import settings


OWNERSHIP_REQUIRED_CALLABLE = getattr(settings, 'OWNERSHIP_REQUIRED_CALLABLE', 'is_owner')

def ownership_required(model, **querys):
    def decorator(func):
        def view(request, *args, **kwargs):
            query = querys.copy()

            for k, v in query.items():
                if v in kwargs:
                    query[k] = kwargs[v]

            obj = get_object_or_404(model, **query)
            kwargs[v] = obj

            if not hasattr(model, OWNERSHIP_REQUIRED_CALLABLE):
                raise ImproperlyConfigured('"%s" doesn\'t have requried callable' % model.__name__)

            attr = getattr(model, OWNERSHIP_REQUIRED_CALLABLE)
            if not callable(attr):
                raise ImproperlyConfigured('"%s" attribute is not callable' % attr.__name__)

            result = attr(obj, request)
            if request.user.is_superuser:
                result = True

            if not result:
                raise PermissionDenied

            return func(request, *args, **kwargs)
        return wraps(func)(view)
    return decorator
