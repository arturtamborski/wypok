from django.conf.urls import include, url

from . import settings
from . import views
from . import apps


app_name = apps.TagsConfig.name

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^add/$', views.create, name='create'),

    url(r'^(?P<tag>' + settings.REGEX + r')/', include([
        url(r'^$', views.show, name='show'),
        url(r'^edit/$', views.update, name='update'),
        url(r'^delete/$', views.delete, name='delete'),
    ])),
]
