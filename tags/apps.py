from django.apps import AppConfig


class TagsConfig(AppConfig):
    name = 'tags'

    def ready(self):
        from tags import signals
