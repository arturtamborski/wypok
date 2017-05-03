from django.conf.urls import url
from . import views
from . import apps


app_name = apps.ExcavationConfig.name
urlpatterns = [
    url(r'^$',                                      views.home, name='home'),
    url(r'^(?P<post_id>[0-9]+)/$',                  views.post, name='post'),
    url(r'^(?P<post_id>[0-9]+)/(?P<slug>\w+)/$',    views.post, name='post'),
]
