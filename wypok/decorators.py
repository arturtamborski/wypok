from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from django.contrib.auth import get_user_model
from django.conf import settings


OWNERSHIP_REQUIRED_CALLABLE = getattr(settings, 'OWNERSHIP_REQUIRED_CALLABLE', 'is_owner')

def ownership_required(model):
    def _decorator(func):
        def _view(request, *args, **kwargs):
            if hasattr(model, OWNERSHIP_REQUIRED_CALLABLE):
                attr = getattr(model, OWNERSHIP_REQUIRED_CALLABLE)
                if attr(model, request, **kwargs):
                    return func(request, *args, **kwargs)
                raise PermissionDenied
            raise ImproperlyConfigured('Provided model "%s" doesn\'t have requried callable for checking ownership.' % model.__name__)
        return _view
    return _decorator
