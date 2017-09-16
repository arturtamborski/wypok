from django.conf.urls import include, url

from posts.apps import PostsConfig
from posts.views import redir, detail, listing, create, update, delete


app_name = PostsConfig.name
urlpatterns = [
    url(r'^$', listing, name='listing'),
    url(r'^add/$', create, name='create'),

    url(r'^(?P<id>[0-9]+)/', include([
        url(r'^$', redir, name='detail'),
        url(r'^edit/$', redir, name='update'),
        url(r'^delete/$', redir, name='delete'),
    ])),

    url(r'^(?P<id>[0-9]+)/(?P<slug>[-a-zA-Z0-9_]+)/', include([
        url(r'^$', detail, name='detail'),
        url(r'^edit/$', update, name='update'),
        url(r'^delete/$', delete, name='delete'),

        url(r'^', include('comments.urls')),
    ])),
]
