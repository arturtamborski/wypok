from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^accounts/(?P<profile>[a-zA-Z][a-zA-Z0-9_-]{3,19})/$', views.profile, name='account_profile'),
]
