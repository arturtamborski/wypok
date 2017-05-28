from functools import wraps

from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from django.shortcuts import get_object_or_404
from django.conf import settings


OWNERSHIP_REQUIRED_CALLABLE = getattr(settings, 'OWNERSHIP_REQUIRED_CALLABLE', 'is_owner')
OWNERSHIP_REQUIRED_PASS_OBJ = getattr(settings, 'OWNERSHIP_REQUIRED_PASS_OBJ', True)

def ownership_required(model, **querys):
    """
    ownership_required - decorator for views used for checking ownership of requested object
    https://arturtamborski.pl/posts/ownership_required-decorator-for-function-based-views-in-django/

    Params:
        - model - model to check ownership
        - querys - query to get_object_or_404 for getting object to test

    Returns:
        decorated function if OWNERSHIP_REQUIRED_CALLABLE from model returned True

    Raises:
        Http404 if query cant find an object
        ImproperlyConfigured if model dosent have OWNERSHIP_REQUIRED_CALLABLE or when its not callable
        PermissionDenied if OWNERSHIP_REQUIRED_CALLABLE returned False

    Settings:
        OWNERSHIP_REQUIRED_CALLABLE - callable that will be used for checking ownership. Defaults to `is_owner`
        OWNERSHIP_REQUIRED_PASS_OBJ - determines wheter to pass found object as last param to view or not

    Usage:
        class Profile(models.Model):
            user = models.OneToOneField(User)
            def is_owner(self, request):
                return self.user == request.user

        @ownership_required(Profile, user__username='profile')
        def detail(request, profile):
            # `profile` variable is *not* str, but an actual object
            # that was found with query from decorator
            return render(request, 'profile.html', {'profile': profile})
            ...
    """
    def decorator(func):
        def view(request, *args, **kwargs):
            if not len(querys):
                raise ImproperlyConfigured('ownership_requried received empty queryset')

            query = querys.copy()

            for k, v in query.items():
                if v in kwargs:
                    query[k] = kwargs[v]

            obj = get_object_or_404(model, **query)

            if OWNERSHIP_REQUIRED_PASS_OBJ:
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
