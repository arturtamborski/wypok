from django.conf.urls import include, url

from profiles.views import detail, update, delete
from profiles.apps import ProfilesConfig


app_name = ProfilesConfig.name
urlpatterns = [
    url(r'^@(?P<profile>[a-zA-Z][a-zA-Z0-9-_]{3,19})/', include([
        url(r'^$', detail, name='detail'),
        url(r'^edit/$', update, name='update'),
        url(r'^delete/$', delete, name='delete'),
    ])),
]
