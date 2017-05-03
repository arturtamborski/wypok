from django.apps import AppConfig


class ExcavationConfig(AppConfig):
    name = 'excavation'

    def ready(self):
        from . import signals
