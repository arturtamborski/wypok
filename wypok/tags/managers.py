from django.db import models


class TagQuerySet(models.QuerySet):
    def get_one(name, owner):
        pass

    def get_few(owner):
        pass
