from django.conf.urls import include, url

from sections.views import home, detail, listing, create, update, delete
from sections.apps import SectionsConfig


app_name = SectionsConfig.name
urlpatterns = [
    url(r'^$', listing, name='listing'),
    url(r'^$', home, name='home'),
    url(r'^new/$', create, name='create'),

    url(r'^(?P<section>[a-zA-Z][a-zA-Z0-9]+)/', include([
        url(r'^$', detail, name='detail'),
        url(r'^edit/$', update, name='update'),
        url(r'^delete/$', delete, name='delete'),

        url(r'^', include('posts.urls')),
    ])),
]
