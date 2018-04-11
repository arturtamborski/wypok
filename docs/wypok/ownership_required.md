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
```
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
