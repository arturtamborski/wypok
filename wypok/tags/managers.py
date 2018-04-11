from django.db import models
from django.core import exceptions

from wypok.utils.ownership_required import is_owner
from wypok.utils.membership_required import is_member


class TagQuerySet(models.QuerySet):

    def get_all(self, user):
        if not is_member(user, 'green'):
            raise exceptions.PermissionDenied

        return self.all()

    def get_one(self, name, user):
        obj = self.get(name=name)

        if not is_owner(user, obj):
            raise exceptions.PermissionDenied

        return obj
