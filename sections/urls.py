from django.conf.urls import url
from . import views
from . import apps


app_name = apps.SectionsConfig.name
urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^(?P<section>[-a-zA-Z0-9_]+)/$', views.home, name='home'),
    url(r'^(?P<section>[-a-zA-Z0-9_]+)/new/$', views.new_post, name='new_post'),
    url(r'^(?P<section>[-a-zA-Z0-9_]+)/(?P<id>[0-9]+)/$', views.post, name='post'),
    url(r'^(?P<section>[-a-zA-Z0-9_]+)/(?P<id>[0-9]+)/edit/$', views.edit_post, name='edit_post'),
    url(r'^(?P<section>[-a-zA-Z0-9_]+)/(?P<id>[0-9]+)/(?P<slug>[-a-zA-Z0-9_]+)/$', views.post, name='post'),
    url(r'^(?P<section>[-a-zA-Z0-9_]+)/(?P<id>[0-9]+)/(?P<slug>[-a-zA-Z0-9_]+)/edit/$', views.edit_post, name='edit_post'),
]
