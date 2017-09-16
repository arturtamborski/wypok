from django.conf.urls import include, url

from notifications.views import listing
from notifications.apps import NotificationsConfig


app_name = NotificationsConfig.name
urlpatterns = [
    url(r'^$', listing, name='listing'),
]
