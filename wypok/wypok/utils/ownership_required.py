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
    """
    ownership_required - decorator for views used for checking ownership of requested object
    https://arturtamborski.pl/posts/ownership_required-decorator-for-function-based-views-in-django/

    Params:
        - model - model to check ownership
        - raise_exception - set to False to fail siliently even if ownership test fails
        - query - query to get_object_or_404 for getting object to test

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
