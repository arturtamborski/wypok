from django.conf.urls import include, url

from tags.views import listing, detail, create, update, delete
from tags.apps import TagsConfig


app_name = TagsConfig.name
urlpatterns = [
    url(r'^$', listing, name='listing'),
    url(r'^add/$', create, name='create'),
    url(r'^(?P<tag>[a-zA-Z0-9_]{3,63})/', include([
        url(r'^$', detail, name='detail'),
        url(r'^edit/$', update, name='update'),
        url(r'^delete/$', delete, name='delete'),
    ])),
]
