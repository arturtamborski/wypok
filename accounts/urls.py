from django.conf.urls import url
from . import views
from . import apps


app_name = apps.AccountsConfig.name
urlpatterns = [
    url(r'^@(?P<profile>[a-zA-Z][a-zA-Z0-9_-]{3,19})/$', views.profile, name='profile'),
]
