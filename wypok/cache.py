# code from https://www.technomancy.org/python/django-proper-opt-in-caching/
# added compatiblity layer for django >= 1.10
from django.utils.deprecation import MiddlewareMixin
from functools import wraps

class DontCacheMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request._cache_update_cache = False

def mark_for_caching(func):
    @wraps(func)
    def newfunc(request, *args, **kwargs):
        request._cache_update_cache = True
        return func(request, *args, **kwargs)
    return newfunc
