from django.apps import AppConfig


class SectionsConfig(AppConfig):
    name = 'sections'

    def ready(self):
        from sections import signals
