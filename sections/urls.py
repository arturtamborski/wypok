from django.conf.urls import url
from . import views
from . import apps


app_name = apps.SectionsConfig.name
urlpatterns = [
    url(r'^$',                                          views.home, name='home'),
    url(r'^(?P<id>[0-9]+)/$',                           views.post, name='post'),
    url(r'^(?P<id>[0-9]+)/(?P<slug>[-a-zA-Z0-9_]+)/$',  views.post, name='post'),
]
