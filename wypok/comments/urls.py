from django.conf.urls import include, url

from comments.apps import CommentsConfig
from comments.views import listing, detail, create, update, delete


app_name = CommentsConfig.name
urlpatterns = [
    url(r'^$', listing, name='listing'),
    url(r'^add/$', create, name='create'),

    url(r'^(?P<comment>[0-9]+)/', include([
        url(r'^$', detail, name='detail'),
        url(r'^edit/$', update, name='update'),
        url(r'^delete/$', delete, name='delete'),
    ])),
]
