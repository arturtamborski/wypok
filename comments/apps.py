from django.apps import AppConfig


class CommentsConfig(AppConfig):
    name = 'comments'

    def ready(self):
        from comments import signals
