from functools import wraps

from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from django.shortcuts import get_object_or_404
from django.conf import settings


OWNERSHIP_REQUIRED_PASS_OBJ = getattr(settings, 'OWNERSHIP_REQUIRED_PASS_OBJ', True)
OWNERSHIP_REQUIRED_CALLABLE = getattr(settings, 'OWNERSHIP_REQUIRED_CALLABLE', 'get_owner')
OWNERSHIP_REQUIRED_PASS_RESULT = getattr(settings, 'OWNERSHIP_REQUIRED_PASS_RESULT', True)
OWNERSHIP_REQUIRED_RESULT_NAME = getattr(settings, 'OWNERSHIP_REQUIRED_RESULT_NAME', 'is_owner')


def is_owner(user, obj):
    if not hasattr(obj, OWNERSHIP_REQUIRED_CALLABLE):
        raise ImproperlyConfigured('"%s" doesn\'t have requried callable' % obj.__class__.__name__)

    attr = getattr(obj, OWNERSHIP_REQUIRED_CALLABLE)

    if not callable(attr):
        raise ImproperlyConfigured('"%s" attribute is not callable' % attr.__name__)

    return attr() == user or user.is_superuser


def ownership_required(model, raise_exception=True, pass_obj=None, pass_result=None, **query):
    def decorator(func):
        def view(request, *args, **kwargs):
            if not len(query):
                raise ImproperlyConfigured('ownership_requried received empty queryset')

            q = query.copy()

            for k, v in q.items():
                if v in kwargs:
                    q[k] = kwargs[v]

            obj = get_object_or_404(model, **q)

            if pass_obj is not False:
                if OWNERSHIP_REQUIRED_PASS_OBJ or pass_obj:
                    kwargs[v] = obj

            result = is_owner(request.user, obj)

            if not result and raise_exception:
                raise PermissionDenied

            if pass_result is not False:
                if OWNERSHIP_REQUIRED_PASS_RESULT or pass_result:
                    setattr(request, OWNERSHIP_REQUIRED_RESULT_NAME, result)

            return func(request, *args, **kwargs)
        return wraps(func)(view)
    return decorator
