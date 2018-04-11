from django.utils.translation import gettext_lazy as _
from django.apps import AppConfig


class TagsConfig(AppConfig):
    name = 'tags'
    verbose_name = _('Tags')

    def ready(self):
        from tags import signals
